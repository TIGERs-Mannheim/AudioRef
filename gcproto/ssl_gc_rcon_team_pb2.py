# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_gc_rcon_team.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_gc_rcon_pb2 as ssl__gc__rcon__pb2
import ssl_gc_common_pb2 as ssl__gc__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16ssl_gc_rcon_team.proto\x1a\x11ssl_gc_rcon.proto\x1a\x13ssl_gc_common.proto\"Y\n\x10TeamRegistration\x12\x11\n\tteam_name\x18\x01 \x02(\t\x12\x1d\n\tsignature\x18\x02 \x01(\x0b\x32\n.Signature\x12\x13\n\x04team\x18\x03 \x01(\x0e\x32\x05.Team\"\xaa\x01\n\x10TeamToController\x12\x1d\n\tsignature\x18\x01 \x01(\x0b\x32\n.Signature\x12\x18\n\x0e\x64\x65sired_keeper\x18\x02 \x01(\x05H\x00\x12,\n\x10\x61\x64vantage_choice\x18\x03 \x01(\x0e\x32\x10.AdvantageChoiceH\x00\x12\x18\n\x0esubstitute_bot\x18\x04 \x01(\x08H\x00\x12\x0e\n\x04ping\x18\x05 \x01(\x08H\x00\x42\x05\n\x03msg\"M\n\x10\x43ontrollerToTeam\x12,\n\x10\x63ontroller_reply\x18\x01 \x01(\x0b\x32\x10.ControllerReplyH\x00\x42\x05\n\x03msgJ\x04\x08\x02\x10\x03*)\n\x0f\x41\x64vantageChoice\x12\x08\n\x04STOP\x10\x00\x12\x0c\n\x08\x43ONTINUE\x10\x01\x42>Z<github.com/RoboCup-SSL/ssl-game-controller/internal/app/rcon')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ssl_gc_rcon_team_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z<github.com/RoboCup-SSL/ssl-game-controller/internal/app/rcon'
  _globals['_ADVANTAGECHOICE']._serialized_start=409
  _globals['_ADVANTAGECHOICE']._serialized_end=450
  _globals['_TEAMREGISTRATION']._serialized_start=66
  _globals['_TEAMREGISTRATION']._serialized_end=155
  _globals['_TEAMTOCONTROLLER']._serialized_start=158
  _globals['_TEAMTOCONTROLLER']._serialized_end=328
  _globals['_CONTROLLERTOTEAM']._serialized_start=330
  _globals['_CONTROLLERTOTEAM']._serialized_end=407
# @@protoc_insertion_point(module_scope)
