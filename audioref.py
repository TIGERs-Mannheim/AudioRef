#!/usr/bin/env python3

#    Copyright 2023 Felix Weinmann

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
import argparse
import pathlib
import queue
import random
import socket
import struct
import threading
from typing import Optional

import yaml
import simpleaudio
from simpleaudio import PlayObject

import gcproto.ssl_gc_referee_message_pb2 as ssl_referee_message
import gcproto.ssl_gc_common_pb2 as ssl_common
import gcproto.ssl_gc_game_event_pb2 as ssl_game_event
import gcproto.ssl_vision_wrapper_pb2 as ssl_vision_wrapper


def open_multicast_socket(ip, port):
    # Adapted from https://stackoverflow.com/a/1794373 (CC BY-SA 4.0 by Gordon Wrigley)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('' if os.name == 'nt' else ip, port))

    sock.setsockopt(
        socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
        struct.pack('4sl', socket.inet_aton(ip), socket.INADDR_ANY)
    )
    return sock


class SoundPack:

    def __init__(self, sound_pack):
        pack_path = pathlib.Path(sound_pack)
        with (pack_path / 'config.yml').open('r') as file:
            self.config = yaml.safe_load(file)

        self.sounds: dict[str, simpleaudio.WaveObject] = {}
        for path in pack_path.rglob('*.wav'):
            self.sounds[
                str(path.relative_to(pack_path)).replace('\\', '/')
            ] = simpleaudio.WaveObject.from_wave_file(str(path))

    def teamsound(self, msg, team):
        try:
            name = getattr(msg, team).name

            if msg.yellow.name == msg.blue.name:
                raise AttributeError

            if name in self.config['teams']:
                team = name
        except AttributeError:
            pass

        return self.sounds[random.choice(self.config['teams'][team])]

    def get_sound(self, soundlist, msg=None, team=None):
        sounds = []
        for sound in random.choice(soundlist).split():
            if sound == "T":
                sounds.append(self.teamsound(msg, team))
            elif sound == "Y":
                sounds.append(self.teamsound(msg, 'yellow'))
            elif sound == "B":
                sounds.append(self.teamsound(msg, 'blue'))
            else:
                sounds.append(self.sounds[sound])

        return tuple(sounds)


class AudioRef:

    def __init__(self, pack: SoundPack, gc_ip, gc_port, vision_ip, vision_port,
                 max_queue_len=5, placement_distance=200.0):
        self.pack = pack
        self.max_queue_len = max_queue_len
        self.placement_distance = placement_distance
        self.gc_socket = open_multicast_socket(gc_ip, gc_port)
        self.vision_socket = open_multicast_socket(vision_ip, vision_port)

        self.whistle: Optional[PlayObject] = None
        self.sound_queue = queue.Queue()
        self.player_thread = threading.Thread(target=self._queue_player, name='sound player', daemon=True)
        self.player_thread.start()

        self.half_field_size = [4500.0, 3000.0]
        self.geometry_thread = threading.Thread(target=self._geometry_receiver, name='vision receiver', daemon=True)
        self.geometry_thread.start()

        msg = ssl_referee_message.Referee()
        msg.ParseFromString(self.gc_socket.recv(65536))

        self.current = {
            'stage': msg.stage,
            'command': msg.command,
            'next_command': msg.next_command
        }
        self.yellow_cards = [msg.yellow.yellow_cards, msg.yellow.red_cards]
        self.blue_cards = [msg.blue.yellow_cards, msg.blue.red_cards]
        self.current_game_event_timestamp = msg.game_events[0].created_timestamp if len(msg.game_events) > 0 else 0

    def _queue_player(self):
        while True:
            while self.sound_queue.qsize() > self.max_queue_len:
                self.sound_queue.get_nowait()

            if self.whistle and self.whistle.is_playing():
                self.whistle.wait_done()

            soundline: tuple[simpleaudio.WaveObject] = self.sound_queue.get()
            for sound in soundline:
                sound.play().wait_done()

    def _geometry_receiver(self):
        while True:
            wrapper = ssl_vision_wrapper.SSL_WrapperPacket()
            wrapper.ParseFromString(self.vision_socket.recv(65536))
            if wrapper.HasField('geometry'):
                field = wrapper.geometry.field
                self.half_field_size = [field.field_length/2, field.field_width/2]

    def run(self):
        print("AudioRef running...")

        while True:
            msg = ssl_referee_message.Referee()
            msg.ParseFromString(self.gc_socket.recv(65536))

            self.enum_sound(self.command, ssl_referee_message.Referee.Command, msg)
            self.enum_sound(self.stage, ssl_referee_message.Referee.Stage, msg)
            for event in msg.game_events:
                self.game_event(msg, event)
            self.cards(msg, 'yellow', self.yellow_cards)
            self.cards(msg, 'blue', self.blue_cards)
            self.enum_sound(self.next_command, ssl_referee_message.Referee.Command, msg, key='next_command')

    def try_sound(self, key, value_name, msg=None, team=None, queued=True):
        try:
            sound = self.pack.get_sound(self.pack.config[key][value_name], msg=msg, team=team)
        except KeyError:
            return

        if queued:
            self.sound_queue.put(sound)
        else:
            if self.whistle is not None and self.whistle.is_playing():
                self.whistle.stop()

            self.whistle = sound[0].play()

    def enum_sound(self, fn, enum, msg, key: str = None):
        if not key:
            key = enum._enum_type.name.lower()

        value = getattr(msg, key)
        if value == self.current[key]:
            return
        self.current[key] = value

        fn(msg, enum.Name(value).lower())

    def stage(self, msg, stage):
        self.try_sound('stages', stage, msg=msg)

    def command(self, msg, command):
        self.try_sound('whistle', command, msg=msg, queued=False)
        self.try_sound('commands', command, msg=msg)

    def next_command(self, msg, command):
        self.try_sound('next_commands', command, msg=msg)

        if hasattr(msg, 'designated_position'):
            at_goal_line = abs(msg.designated_position.x) == self.half_field_size[0] - self.placement_distance
            at_touch_line = abs(msg.designated_position.y) == self.half_field_size[1] - self.placement_distance

            if at_touch_line:
                if at_goal_line:
                    self.try_sound(command, 'corner_kick', msg=msg)
                else:
                    self.try_sound(command, 'throw_in', msg=msg)
            else:
                self.try_sound(command, 'free_kick', msg=msg)

    def game_event(self, msg, event):
        if event.created_timestamp <= self.current_game_event_timestamp:
            return  # Already handled
        self.current_game_event_timestamp = event.created_timestamp

        typename = ssl_game_event.GameEvent.Type.Name(event.type).lower()
        if typename not in self.pack.config['game_events']:
            return

        try:
            team = ssl_common.Team.Name(getattr(event, typename).by_team).lower()
        except AttributeError:
            team = None

        self.try_sound('game_events', typename, msg=msg, team=team)

    def cards(self, msg, team, current_cards):
        team_info = getattr(msg, team)

        yellow_cards = team_info.yellow_cards
        if yellow_cards > current_cards[0]:
            current_cards[0] += 1
            self.sound_queue.put(self.pack.get_sound(self.pack.config['yellow_card'], msg=msg, team=team))

        red_cards = team_info.red_cards
        if red_cards > current_cards[1]:
            current_cards[1] += 1
            self.sound_queue.put(self.pack.get_sound(self.pack.config['red_card'], msg=msg, team=team))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='AudioRef')
    parser.add_argument('--gc_ip', default='224.5.23.1', help='Multicast IP address of the game controller')
    parser.add_argument('--gc_port', type=int, default=10003, help='Multicast port of the game controller')
    parser.add_argument('--vision_ip', default='224.5.23.2', help='Multicast IP address of the vision')
    parser.add_argument('--vision_port', type=int, default=10006, help='Multicast port of the vision')
    parser.add_argument('--pack', default='sounds/en', help='Path to the sound pack')
    parser.add_argument('--max_queue_len', type=int, default=3, help='Maximum of sounds in the queue')
    args = parser.parse_args()

    print("Starting AudioRef\n")

    try:
        AudioRef(
            SoundPack(args.pack),
            args.gc_ip, args.gc_port,
            args.vision_ip, args.vision_port,
            max_queue_len=args.max_queue_len
        ).run()
    except KeyboardInterrupt:
        print("\nStopping AudioRef")
