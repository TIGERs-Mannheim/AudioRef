#!/usr/bin/env python3

#    Copyright 2023-2024 Felix Weinmann

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
from typing import Callable, Dict, List, Optional, Tuple, TypeVar

from google.protobuf.message import Message
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper
import simpleaudio
import yaml

if any(
        not os.path.exists('proto/' + proto + '_pb2.py')
        for proto in ('ssl_gc_referee_message', 'ssl_gc_common', 'ssl_gc_game_event', 'ssl_vision_wrapper')
):
    print("Compiling Protobuf files...")
    import grpc_tools.protoc
    grpc_tools.protoc.main([
        'protoc',
        '--python_out=.', '--pyi_out=.',
        *[str(path) for path in pathlib.Path().rglob('proto/*.proto')]
    ])

from proto.ssl_gc_referee_message_pb2 import Referee
from proto.ssl_gc_common_pb2 import Team
from proto.ssl_gc_game_event_pb2 import GameEvent
from proto.ssl_vision_wrapper_pb2 import SSL_WrapperPacket


def open_multicast_socket(ip: str, port: int) -> socket.socket:
    # Adapted from https://stackoverflow.com/a/1794373 (CC BY-SA 4.0 by Gordon Wrigley)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Windows does not allow binding UDP sockets to a specific ip address.
    sock.bind(('' if os.name == 'nt' else ip, port))

    sock.setsockopt(
        socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
        struct.pack('4sl', socket.inet_aton(ip), socket.INADDR_ANY)
    )
    return sock

_Message = TypeVar('_Message', bound=Message)
def receive_multicast(sock: socket.socket, msg: _Message) -> Tuple[_Message, str]:
    data, addr = sock.recvfrom(65535)
    msg.ParseFromString(data)
    return msg, addr[0]


class SoundPack:

    def __init__(self, pack_path: pathlib.Path):
        with (pack_path / 'config.yml').open('r') as file:
            self.config = yaml.safe_load(file)

        self.sounds: Dict[str, simpleaudio.WaveObject] = {}
        for path in pack_path.rglob('*.wav'):
            self.sounds[
                str(path.relative_to(pack_path)).replace('\\', '/')
            ] = simpleaudio.WaveObject.from_wave_file(str(path))

    def team_sound(self, msg: Referee, team: str) -> simpleaudio.WaveObject:
        """Returns a corresponding sound for the team using the gc message msg to resolve team names.

        :param msg: Referee message
        :param team: 'yellow', 'blue' or 'unknown'
        :returns: WaveObject corresponding to the team
        """

        # Don't try to use the team name in case both sides have the same name.
        if msg.yellow.name != msg.blue.name:
            name = getattr(msg, team, team).name
            if name in self.config['teams']:
                team = name

        return self.sounds[random.choice(self.config['teams'][team])]

    def get_sound(self, *path: str, msg: Referee=None, team: str=None) -> Tuple[simpleaudio.WaveObject, ...]:
        """Returns a sound line for the given path, replacing placeholders with corresponding team sounds.

        :param path: Path in the config file to the list of sound lines for the event
        :param msg: Referee message
        :param team: 'yellow', 'blue' or 'unknown'
        :raises KeyError: If no sound line exists for the given path
        """

        sound_list = self.config
        for key in path:
            sound_list = sound_list[key]

        sound_line = []
        for sound in random.choice(sound_list).split():
            if sound == "T":
                sound_line.append(self.team_sound(msg, team))
            elif sound == "Y":
                sound_line.append(self.team_sound(msg, 'yellow'))
            elif sound == "B":
                sound_line.append(self.team_sound(msg, 'blue'))
            else:
                sound_line.append(self.sounds[sound])

        return tuple(sound_line)


class AudioRef:

    def __init__(
            self,
            pack: SoundPack,
            gc_ip: str, gc_port: int,
            vision_ip: str, vision_port: int,
            max_queue_len: int=3,
            # Distance in mm from the field boundary for throw in and corner kick detection
            placement_distance: float=200.0
    ):
        self.pack = pack
        self.max_queue_len = max_queue_len
        self.placement_distance = placement_distance
        self.gc_socket = open_multicast_socket(gc_ip, gc_port)
        self.vision_socket = open_multicast_socket(vision_ip, vision_port)

        self.immediate_sound: Optional[simpleaudio.PlayObject] = None
        self.sound_queue = queue.Queue()
        self.player_thread = threading.Thread(target=self._queue_player, name='sound player', daemon=True)
        self.player_thread.start()

        self.half_field_size = [4500.0, 3000.0]
        self.cam_ips = {}
        self.geometry_thread = threading.Thread(target=self._geometry_receiver, name='vision receiver', daemon=True)
        self.geometry_thread.start()

        # Initialize the current state to prevent sound spam when restarting the AudioRef mid-game
        print("Waiting for referee message...")
        msg, self.gc_ip = receive_multicast(self.gc_socket, Referee())

        self.current = {
            'stage': msg.stage,
            'command': msg.command,
            'next_command': msg.next_command
        }
        self.cards_yellow = [msg.yellow.yellow_cards, msg.yellow.red_cards]
        self.cards_blue = [msg.blue.yellow_cards, msg.blue.red_cards]
        self.current_game_event_timestamp = msg.game_events[0].created_timestamp if len(msg.game_events) > 0 else 0

    def _queue_player(self):
        """Sound queue player thread"""
        while True:
            while self.sound_queue.qsize() > self.max_queue_len:
                self.sound_queue.get_nowait()

            if self.immediate_sound and self.immediate_sound.is_playing():
                self.immediate_sound.wait_done()

            sound_line: tuple[simpleaudio.WaveObject] = self.sound_queue.get()
            for sound in sound_line:
                sound.play().wait_done()

    def _geometry_receiver(self):
        """SSL-Vision geometry receiver thread"""
        while True:
            wrapper, ip = receive_multicast(self.vision_socket, SSL_WrapperPacket())

            if wrapper.HasField('geometry'):
                field = wrapper.geometry.field
                self.half_field_size = [field.field_length/2, field.field_width/2]
            else:
                cam_id = wrapper.detection.camera_id
                if cam_id in self.cam_ips and self.cam_ips[cam_id] != ip:
                    self.play_sound('duplicate_vision')
                self.cam_ips[cam_id] = ip

    def run(self):
        """SSL-game controller receiver and sound queueing method"""
        print("Initialized. AudioRef running")

        while True:
            msg, ip = receive_multicast(self.gc_socket, Referee())
            if self.gc_ip == '127.0.0.1':
                self.gc_ip = ip

            if ip != '127.0.0.1' and ip != self.gc_ip:
                self.play_sound('duplicate_gamecontroller')
                self.gc_ip = ip
                continue  # Do not spam frequent state changes due to toggling gamecontroller

            self.enum_sound(self.command, Referee.Command, msg)
            self.enum_sound(self.stage, Referee.Stage, msg)
            for event in msg.game_events:
                self.game_event(msg, event)
            self.cards(msg, 'yellow', self.cards_yellow)
            self.cards(msg, 'blue', self.cards_blue)
            self.enum_sound(self.next_command, Referee.Command, msg, key='next_command')

    def play_sound(self, *path: str, msg: Referee=None, team: str=None, queued: bool=True):
        """Tries to play a sound line at the config path if it exists.

        :param path: Path in the config to the sound line list
        :param msg: Referee message
        :param team: 'yellow', 'blue' or 'unknown'
        :param queued: If the sound line should be added to the queue or played immediately
        """
        try:
            sound = self.pack.get_sound(*path, msg=msg, team=team)
        except KeyError:
            return  # No sound line available

        if queued:
            self.sound_queue.put(sound)
        else:
            if self.immediate_sound is not None and self.immediate_sound.is_playing():
                self.immediate_sound.stop()

            self.immediate_sound = sound[0].play()

    def enum_sound(self, fn: Callable[[Referee, str], None], enum: EnumTypeWrapper, msg: Referee, key: str=None):
        """Generic method for enum based sound triggers (Commands, Stages)

        :param fn: (msg, enum_value_name) Function to call in case of a change in the enum value
        :param enum: Protobuf enum class
        :param msg: Referee message
        :param key: key of the enum value in the Referee message in cases the enum name differs from the enum name
        """
        if not key:
            key = enum.DESCRIPTOR.name.lower()

        value = getattr(msg, key)
        if value == self.current[key]:
            return
        self.current[key] = value

        fn(msg, enum.Name(value).lower())

    def stage(self, msg: Referee, stage: str):
        self.play_sound('stages', stage, msg=msg)

    def command(self, msg: Referee, command: str):
        self.play_sound('whistle', command, msg=msg, queued=False)
        self.play_sound('commands', command, msg=msg)

    def next_command(self, msg: Referee, command: str):
        self.play_sound('next_commands', command, msg=msg)

        if hasattr(msg, 'designated_position'):
            at_goal_line = abs(msg.designated_position.x) == self.half_field_size[0] - self.placement_distance
            at_touch_line = abs(msg.designated_position.y) == self.half_field_size[1] - self.placement_distance

            if at_touch_line:
                if at_goal_line:
                    self.play_sound(command, 'corner_kick', msg=msg)
                else:
                    self.play_sound(command, 'throw_in', msg=msg)
            else:
                self.play_sound(command, 'free_kick', msg=msg)

    def game_event(self, msg: Referee, event: GameEvent):
        if event.created_timestamp <= self.current_game_event_timestamp:
            return  # Already handled
        self.current_game_event_timestamp = event.created_timestamp

        typename = GameEvent.Type.Name(event.type).lower()
        if typename not in self.pack.config['game_events']:
            return

        try:
            team = Team.Name(getattr(event, typename).by_team).lower()
        except AttributeError:
            team = None

        self.play_sound('game_events', typename, msg=msg, team=team)

    def cards(self, msg: Referee, team: str, current_cards: List[int]):
        team_info = getattr(msg, team)

        yellow_cards = team_info.yellow_cards
        if yellow_cards > current_cards[0]:
            current_cards[0] += 1
            self.play_sound('yellow_card', msg=msg, team=team)
        else:
            current_cards[0] = yellow_cards

        red_cards = team_info.red_cards
        if red_cards > current_cards[1]:
            current_cards[1] += 1
            self.play_sound('red_card', msg=msg, team=team)
        else:
            current_cards[1] = red_cards


def anti_standby_sound():
    from time import sleep
    sound = simpleaudio.WaveObject.from_wave_file(str(pathlib.Path(__file__).parent / "anti_standby_sound.wav"))
    while True:
        sleep(1.0)
        sound.play()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='AudioRef')
    # When editing the arguments also edit the corresponding section in README.md
    parser.add_argument('--gc_ip', default='224.5.23.1', help='Multicast IP address of the game controller (default: 224.5.23.1)')
    parser.add_argument('--gc_port', type=int, default=10003, help='Multicast port of the game controller (default: 10003)')
    parser.add_argument('--vision_ip', default='224.5.23.2', help='Multicast IP address of the vision (default: 224.5.23.2)')
    parser.add_argument('--vision_port', type=int, default=10006, help='Multicast port of the vision (default: 10006)')
    parser.add_argument('--pack', default='sounds/en', type=pathlib.Path, help='Path to the sound pack (default: sounds/en)')
    parser.add_argument('--max_queue_len', type=int, default=3, help='Maximum amount of sound lines in the queue (default: 3)')
    parser.add_argument('--anti_standby_sound', action='store_true', help='Plays a quiet very low frequency sound to prevent battery powered speakers from switching into standby mode (default: false)')
    args = parser.parse_args()

    if args.anti_standby_sound:
        threading.Thread(target=anti_standby_sound, name='anti standby sound', daemon=True).start()

    try:
        AudioRef(
            SoundPack(args.pack),
            args.gc_ip, args.gc_port,
            args.vision_ip, args.vision_port,
            max_queue_len=args.max_queue_len
        ).run()
    except KeyboardInterrupt:
        print("Stopping AudioRef")
