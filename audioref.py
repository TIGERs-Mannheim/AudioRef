import argparse
import pathlib
import queue
import random
import socket
import struct
import threading

import yaml
import simpleaudio

import gcproto.ssl_gc_referee_message_pb2 as ssl_referee_message
import gcproto.ssl_gc_common_pb2 as ssl_common
import gcproto.ssl_gc_game_event_pb2 as ssl_game_event


def open_multicast_socket(ip, port):
    # https://stackoverflow.com/a/1794373 CC BY-SA 4.0 Gordon Wrigley
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((ip, port))

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

            team = name if name in self.config['teams'] else team
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

    def __init__(self, pack: SoundPack, ip, port, max_queue_len=5):
        self.pack = pack
        self.max_queue_len = max_queue_len
        self.sock = open_multicast_socket(ip, port)

        self.sound_queue = queue.Queue()
        self.player_thread = threading.Thread(target=self._queue_player, name='sound player', daemon=True)
        self.player_thread.start()

        self.current_game_event_timestamp = 0
        self.current_stage = ssl_referee_message.Referee.Stage.NORMAL_FIRST_HALF_PRE
        self.current_command = ssl_referee_message.Referee.Command.HALT
        self.yellow_cards = [0, 0]
        self.blue_cards = [0, 0]

    def _queue_player(self):
        while True:
            while self.sound_queue.qsize() > self.max_queue_len:
                self.sound_queue.get_nowait()

            soundline: tuple[simpleaudio.WaveObject] = self.sound_queue.get()
            for sound in soundline:
                sound.play().wait_done()

    def run(self):
        while True:
            msg = ssl_referee_message.Referee()
            msg.ParseFromString(self.sock.recv(10240))

            self.stage(msg)
            self.command(msg)
            for event in msg.game_events:
                self.game_event(msg, event)
            self.cards(msg, 'yellow', self.yellow_cards)
            self.cards(msg, 'blue', self.blue_cards)

    def stage(self, msg):
        stage = msg.stage
        if stage == self.current_stage:
            return
        self.current_stage = stage

        stagename = ssl_referee_message.Referee.Stage.Name(stage).lower()

        try:
            self.sound_queue.put(self.pack.get_sound(self.pack.config['stages'][stagename]))
        except KeyError:
            pass

    def command(self, msg):
        command = msg.command
        if command == self.current_command:
            return
        self.current_command = command

        commandname = ssl_referee_message.Referee.Command.Name(command).lower()

        try:
            self.pack.get_sound(self.pack.config['whistle'][commandname], msg=msg)[0].play()
        except KeyError:
            pass

        try:
            self.sound_queue.put(self.pack.get_sound(self.pack.config['commands'][commandname], msg=msg))
        except KeyError:
            pass

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

        self.sound_queue.put(self.pack.get_sound(self.pack.config['game_events'][typename], msg=msg, team=team))

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
    parser.add_argument('--pack', default='sounds/de', help='Path to the sound pack')
    parser.add_argument('--max_queue_len', type=int, default=5, help='Maximum of sounds in the queue')
    args = parser.parse_args()

    AudioRef(SoundPack(args.pack), args.gc_ip, args.gc_port, max_queue_len=args.max_queue_len).run()
