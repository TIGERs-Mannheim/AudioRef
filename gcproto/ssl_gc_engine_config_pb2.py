# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_gc_engine_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1assl_gc_engine_config.proto\"\xec\x03\n\x06\x43onfig\x12;\n\x13game_event_behavior\x18\x01 \x03(\x0b\x32\x1e.Config.GameEventBehaviorEntry\x12\x35\n\x10\x61uto_ref_configs\x18\x02 \x03(\x0b\x32\x1b.Config.AutoRefConfigsEntry\x12\x1d\n\x15\x61\x63tive_tracker_source\x18\x03 \x01(\t\x12\r\n\x05teams\x18\x04 \x03(\t\x12\x15\n\rauto_continue\x18\x05 \x01(\x08\x1aJ\n\x16GameEventBehaviorEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0e\x32\x10.Config.Behavior:\x02\x38\x01\x1a\x45\n\x13\x41utoRefConfigsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1d\n\x05value\x18\x02 \x01(\x0b\x32\x0e.AutoRefConfig:\x02\x38\x01\"\x95\x01\n\x08\x42\x65havior\x12\x14\n\x10\x42\x45HAVIOR_UNKNOWN\x10\x00\x12\x13\n\x0f\x42\x45HAVIOR_ACCEPT\x10\x01\x12\x1c\n\x18\x42\x45HAVIOR_ACCEPT_MAJORITY\x10\x02\x12\x19\n\x15\x42\x45HAVIOR_PROPOSE_ONLY\x10\x03\x12\x10\n\x0c\x42\x45HAVIOR_LOG\x10\x04\x12\x13\n\x0f\x42\x45HAVIOR_IGNORE\x10\x05\"\x84\x02\n\rAutoRefConfig\x12\x42\n\x13game_event_behavior\x18\x01 \x03(\x0b\x32%.AutoRefConfig.GameEventBehaviorEntry\x1aQ\n\x16GameEventBehaviorEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0e\x32\x17.AutoRefConfig.Behavior:\x02\x38\x01\"\\\n\x08\x42\x65havior\x12\x14\n\x10\x42\x45HAVIOR_UNKNOWN\x10\x00\x12\x13\n\x0f\x42\x45HAVIOR_ACCEPT\x10\x01\x12\x10\n\x0c\x42\x45HAVIOR_LOG\x10\x02\x12\x13\n\x0f\x42\x45HAVIOR_IGNORE\x10\x03\x42@Z>github.com/RoboCup-SSL/ssl-game-controller/internal/app/engine')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ssl_gc_engine_config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z>github.com/RoboCup-SSL/ssl-game-controller/internal/app/engine'
  _CONFIG_GAMEEVENTBEHAVIORENTRY._options = None
  _CONFIG_GAMEEVENTBEHAVIORENTRY._serialized_options = b'8\001'
  _CONFIG_AUTOREFCONFIGSENTRY._options = None
  _CONFIG_AUTOREFCONFIGSENTRY._serialized_options = b'8\001'
  _AUTOREFCONFIG_GAMEEVENTBEHAVIORENTRY._options = None
  _AUTOREFCONFIG_GAMEEVENTBEHAVIORENTRY._serialized_options = b'8\001'
  _globals['_CONFIG']._serialized_start=31
  _globals['_CONFIG']._serialized_end=523
  _globals['_CONFIG_GAMEEVENTBEHAVIORENTRY']._serialized_start=226
  _globals['_CONFIG_GAMEEVENTBEHAVIORENTRY']._serialized_end=300
  _globals['_CONFIG_AUTOREFCONFIGSENTRY']._serialized_start=302
  _globals['_CONFIG_AUTOREFCONFIGSENTRY']._serialized_end=371
  _globals['_CONFIG_BEHAVIOR']._serialized_start=374
  _globals['_CONFIG_BEHAVIOR']._serialized_end=523
  _globals['_AUTOREFCONFIG']._serialized_start=526
  _globals['_AUTOREFCONFIG']._serialized_end=786
  _globals['_AUTOREFCONFIG_GAMEEVENTBEHAVIORENTRY']._serialized_start=611
  _globals['_AUTOREFCONFIG_GAMEEVENTBEHAVIORENTRY']._serialized_end=692
  _globals['_AUTOREFCONFIG_BEHAVIOR']._serialized_start=694
  _globals['_AUTOREFCONFIG_BEHAVIOR']._serialized_end=786
# @@protoc_insertion_point(module_scope)
