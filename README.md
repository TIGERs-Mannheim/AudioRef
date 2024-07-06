# AudioRef

A voice for the game controller!
Listens for game controller and vision packets and plays appropriate acoustic signals.

## Dependencies

- Python 3.5 or newer
- `grpcio-tools`
  (Optional when compiling the protobuf files manually with `protoc --python_out=. --pyi_out=. proto/*.proto`)
- `pyyaml`
- `protobuf`
- `simpleaudio` (in case of issues with `simpleaudio` and Python 3.12 use `simpleaudio-patched`)


## Usage

Linux, macOS: `./audioref.py` \
Windows: `python audioref.py`

For a list of available options add ` --help`.


## Creating a sound pack

A sound pack is a folder containing `.wav` sound files and an `config.yml` file with the following structure
(all entries except for `teams` are optional):

- `teams` sounds are embedded into other sound lines.
  Entries are named after the team names sent by the game controller (case-sensitive), `yellow`, `blue` or `unknown`.
  If no corresponding sounds are given for the specific team name sent by the game controller
  (or both teams have the same name) the sound lines for `yellow` or `blue` are used.
  `unknown` is used by the game controller in cases the trigger cannot be attributed to a single team.

- `stages` sound lines are triggered on stage changes.
  Possible entries are the values of the
  [ssl_gc_referee_message.proto:21 Referee.Stage](proto/ssl_gc_referee_message.proto) enum (in lower case).
- `commands` sound lines are triggered on command changes.
  Possible entries are the values of the
  [ssl_gc_referee_message.proto:77 Referee.Command](proto/ssl_gc_referee_message.proto) enum (in lower case).
- `whistle` sound lines are triggered on command changes.
  Possible entries are the values of the
  [ssl_gc_referee_message.proto:77 Referee.Command](proto/ssl_gc_referee_message.proto) enum (in lower case).
  In contrast to all other sounds, whistle sounds play immediately
  (and interrupt the already running immediate sound if necessary).
  Only the first sound of the sound line is played.
- `next_commands` sound lines are triggered by changes in the `next_command` field.
  Possible entries are the values of the
  [ssl_gc_referee_message.proto:77 Referee.Command](proto/ssl_gc_referee_message.proto) enum (in lower case).
- `direct_free_yellow` and `direct_free_blue` sound lines are played
  if the next_command field is changed to the corresponding value.
  This additional field allows for separate sound lines to be played depending on the designated (ball) position:
  - `corner_kick` if the position is 200mm inwards from a touch line and goal line.
  - `throw_in` if the position is 200mm inwards from a touch line.
  - `free_kick` if the position is somewhere else on the field.
- `game_events` are triggered by new game events,
  possible entries are the values of the
  [ssl_gc_game_event.proto:522 GameEvent.Type](proto/ssl_gc_game_event.proto) enum (in lower case).
- `yellow_card` sound lines are played for each yellow card counter increment.
- `red_card` sound lines are played for each red card counter increment.

A *sound line* is one or more sounds separated by a space character to build compound sounds for events,
e.g.: `foul.wav T keeper_held_ball.wav`.
A single sound line is chosen at random during playback in case multiple sound lines exist for a single config entry.

A *sound* is one of the following:
- `path/to/sound.wav`: Path of a wav sound file relative to the sound pack folder.
  All sound files need to be inside the sound pack folder.
- `Y`: Wildcard for a sound for the yellow team
- `B`: Wildcard for a sound for the blue team 
- `T`: Wildcard for a sound for the corresponding team (if applicable, e.g. fouls)

Example config file: [sounds/en/config.yml](sounds/en/config.yml).

If you want to contribute your sound pack to this repository please append your copyright and license notice
for the sound pack at the end of [LICENSE.md](LICENSE.md).
