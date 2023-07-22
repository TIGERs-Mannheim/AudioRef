# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_gc_state.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_gc_common_pb2 as ssl__gc__common__pb2
import ssl_gc_geometry_pb2 as ssl__gc__geometry__pb2
import ssl_gc_game_event_pb2 as ssl__gc__game__event__pb2
import ssl_gc_referee_message_pb2 as ssl__gc__referee__message__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12ssl_gc_state.proto\x1a\x13ssl_gc_common.proto\x1a\x15ssl_gc_geometry.proto\x1a\x17ssl_gc_game_event.proto\x1a\x1cssl_gc_referee_message.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"u\n\nYellowCard\x12\n\n\x02id\x18\x01 \x01(\r\x12(\n\x14\x63\x61used_by_game_event\x18\x02 \x01(\x0b\x32\n.GameEvent\x12\x31\n\x0etime_remaining\x18\x03 \x01(\x0b\x32\x19.google.protobuf.Duration\"?\n\x07RedCard\x12\n\n\x02id\x18\x01 \x01(\r\x12(\n\x14\x63\x61used_by_game_event\x18\x02 \x01(\x0b\x32\n.GameEvent\"k\n\x04\x46oul\x12\n\n\x02id\x18\x01 \x01(\r\x12(\n\x14\x63\x61used_by_game_event\x18\x02 \x01(\x0b\x32\n.GameEvent\x12-\n\ttimestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xd9\x01\n\x07\x43ommand\x12\x1b\n\x04type\x18\x01 \x02(\x0e\x32\r.Command.Type\x12\x17\n\x08\x66or_team\x18\x02 \x02(\x0e\x32\x05.Team\"\x97\x01\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04HALT\x10\x01\x12\x08\n\x04STOP\x10\x02\x12\x10\n\x0cNORMAL_START\x10\x03\x12\x0f\n\x0b\x46ORCE_START\x10\x04\x12\n\n\x06\x44IRECT\x10\x05\x12\x0b\n\x07KICKOFF\x10\x07\x12\x0b\n\x07PENALTY\x10\x08\x12\x0b\n\x07TIMEOUT\x10\t\x12\x12\n\x0e\x42\x41LL_PLACEMENT\x10\n\"\x04\x08\x06\x10\x06\"\xc3\x01\n\tGameState\x12\x1d\n\x04type\x18\x01 \x02(\x0e\x32\x0f.GameState.Type\x12\x17\n\x08\x66or_team\x18\x02 \x01(\x0e\x32\x05.Team\"~\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04HALT\x10\x01\x12\x08\n\x04STOP\x10\x02\x12\x0b\n\x07RUNNING\x10\x03\x12\r\n\tFREE_KICK\x10\x04\x12\x0b\n\x07KICKOFF\x10\x05\x12\x0b\n\x07PENALTY\x10\x06\x12\x0b\n\x07TIMEOUT\x10\x07\x12\x12\n\x0e\x42\x41LL_PLACEMENT\x10\x08\"Y\n\x08Proposal\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1e\n\ngame_event\x18\x02 \x01(\x0b\x32\n.GameEvent\"?\n\rProposalGroup\x12\x1c\n\tproposals\x18\x01 \x03(\x0b\x32\t.Proposal\x12\x10\n\x08\x61\x63\x63\x65pted\x18\x02 \x01(\x08\"\xf3\x04\n\x08TeamInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05goals\x18\x02 \x01(\x05\x12\x12\n\ngoalkeeper\x18\x03 \x01(\x05\x12!\n\x0cyellow_cards\x18\x04 \x03(\x0b\x32\x0b.YellowCard\x12\x1b\n\tred_cards\x18\x05 \x03(\x0b\x32\x08.RedCard\x12\x15\n\rtimeouts_left\x18\x06 \x01(\x05\x12\x34\n\x11timeout_time_left\x18\x07 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x18\n\x10on_positive_half\x18\x08 \x01(\x08\x12\x14\n\x05\x66ouls\x18\t \x03(\x0b\x32\x05.Foul\x12\x1f\n\x17\x62\x61ll_placement_failures\x18\n \x01(\x05\x12\'\n\x1f\x62\x61ll_placement_failures_reached\x18\x0b \x01(\x08\x12\x16\n\x0e\x63\x61n_place_ball\x18\x0c \x01(\x08\x12\x18\n\x10max_allowed_bots\x18\r \x01(\x05\x12\x43\n\x1frequests_bot_substitution_since\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12:\n\x16requests_timeout_since\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x41\n\x1drequests_emergency_stop_since\x18\x10 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x17\n\x0f\x63hallenge_flags\x18\x11 \x01(\x05\x12 \n\x18\x62ot_substitution_allowed\x18\x12 \x01(\x08\"\xfe\x05\n\x05State\x12\x1d\n\x05stage\x18\x01 \x01(\x0e\x32\x0e.Referee.Stage\x12\x19\n\x07\x63ommand\x18\x02 \x01(\x0b\x32\x08.Command\x12\x1e\n\ngame_state\x18\x13 \x01(\x0b\x32\n.GameState\x12\x35\n\x12stage_time_elapsed\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x32\n\x0fstage_time_left\x18\x05 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x34\n\x10match_time_start\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12)\n\nteam_state\x18\x08 \x03(\x0b\x32\x15.State.TeamStateEntry\x12\x1f\n\rplacement_pos\x18\t \x01(\x0b\x32\x08.Vector2\x12\x1e\n\x0cnext_command\x18\n \x01(\x0b\x32\x08.Command\x12@\n\x1d\x63urrent_action_time_remaining\x18\x0c \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x1f\n\x0bgame_events\x18\r \x03(\x0b\x32\n.GameEvent\x12\'\n\x0fproposal_groups\x18\x0e \x03(\x0b\x32\x0e.ProposalGroup\x12\x1b\n\x08\x64ivision\x18\x0f \x01(\x0e\x32\t.Division\x12!\n\x12\x66irst_kickoff_team\x18\x11 \x01(\x0e\x32\x05.Team\x12\x1e\n\nmatch_type\x18\x12 \x01(\x0e\x32\n.MatchType\x12\x37\n\x13ready_continue_time\x18\x14 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12&\n\x0eshootout_state\x18\x15 \x01(\x0b\x32\x0e.ShootoutState\x1a;\n\x0eTeamStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x18\n\x05value\x18\x02 \x01(\x0b\x32\t.TeamInfo:\x02\x38\x01J\x04\x08\x10\x10\x11\"\xa4\x01\n\rShootoutState\x12\x18\n\tnext_team\x18\x01 \x01(\x0e\x32\x05.Team\x12@\n\x12number_of_attempts\x18\x02 \x03(\x0b\x32$.ShootoutState.NumberOfAttemptsEntry\x1a\x37\n\x15NumberOfAttemptsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x42?Z=github.com/RoboCup-SSL/ssl-game-controller/internal/app/state')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ssl_gc_state_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z=github.com/RoboCup-SSL/ssl-game-controller/internal/app/state'
  _STATE_TEAMSTATEENTRY._options = None
  _STATE_TEAMSTATEENTRY._serialized_options = b'8\001'
  _SHOOTOUTSTATE_NUMBEROFATTEMPTSENTRY._options = None
  _SHOOTOUTSTATE_NUMBEROFATTEMPTSENTRY._serialized_options = b'8\001'
  _globals['_YELLOWCARD']._serialized_start=186
  _globals['_YELLOWCARD']._serialized_end=303
  _globals['_REDCARD']._serialized_start=305
  _globals['_REDCARD']._serialized_end=368
  _globals['_FOUL']._serialized_start=370
  _globals['_FOUL']._serialized_end=477
  _globals['_COMMAND']._serialized_start=480
  _globals['_COMMAND']._serialized_end=697
  _globals['_COMMAND_TYPE']._serialized_start=546
  _globals['_COMMAND_TYPE']._serialized_end=697
  _globals['_GAMESTATE']._serialized_start=700
  _globals['_GAMESTATE']._serialized_end=895
  _globals['_GAMESTATE_TYPE']._serialized_start=769
  _globals['_GAMESTATE_TYPE']._serialized_end=895
  _globals['_PROPOSAL']._serialized_start=897
  _globals['_PROPOSAL']._serialized_end=986
  _globals['_PROPOSALGROUP']._serialized_start=988
  _globals['_PROPOSALGROUP']._serialized_end=1051
  _globals['_TEAMINFO']._serialized_start=1054
  _globals['_TEAMINFO']._serialized_end=1681
  _globals['_STATE']._serialized_start=1684
  _globals['_STATE']._serialized_end=2450
  _globals['_STATE_TEAMSTATEENTRY']._serialized_start=2385
  _globals['_STATE_TEAMSTATEENTRY']._serialized_end=2444
  _globals['_SHOOTOUTSTATE']._serialized_start=2453
  _globals['_SHOOTOUTSTATE']._serialized_end=2617
  _globals['_SHOOTOUTSTATE_NUMBEROFATTEMPTSENTRY']._serialized_start=2562
  _globals['_SHOOTOUTSTATE_NUMBEROFATTEMPTSENTRY']._serialized_end=2617
# @@protoc_insertion_point(module_scope)
