# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: Result.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'Result.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import os
import sys
sys.path.append(os.path.dirname("Buffer"))

import Buffer.Game_pb2 as Game__pb2
import Buffer.Player_pb2 as Player__pb2
import Buffer.GameServer_pb2 as GameServer__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cResult.proto\x12\x0b\x64istributed\x1a\nGame.proto\x1a\x0cPlayer.proto\x1a\x10GameServer.proto\",\n\x06Result\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x9b\x01\n\x08Register\x12#\n\x06player\x18\x01 \x01(\x0b\x32\x13.distributed.Player\x12\x0c\n\x04game\x18\x02 \x01(\x05\x12%\n\x07setting\x18\x03 \x01(\x0b\x32\x14.distributed.Setting\x12%\n\x07\x63ontext\x18\x04 \x01(\x0b\x32\x14.distributed.Context\x12\x0e\n\x06update\x18\x05 \x01(\t\"\x96\x02\n\x08Response\x12#\n\x06result\x18\x01 \x01(\x0b\x32\x13.distributed.Result\x12+\n\ngameServer\x18\x02 \x01(\x0b\x32\x17.distributed.GameServer\x12\x1f\n\x04game\x18\x03 \x01(\x0b\x32\x11.distributed.Game\x12\x19\n\x11gameServerAddress\x18\x04 \x01(\t\x12 \n\x05words\x18\x05 \x01(\x0b\x32\x11.distributed.Word\x12%\n\x07\x63ontext\x18\x06 \x01(\x0b\x32\x14.distributed.Context\x12\x0e\n\x06update\x18\x07 \x01(\t\x12#\n\x06player\x18\x08 \x01(\x0b\x32\x13.distributed.Playerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Result_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RESULT']._serialized_start=73
  _globals['_RESULT']._serialized_end=117
  _globals['_REGISTER']._serialized_start=120
  _globals['_REGISTER']._serialized_end=275
  _globals['_RESPONSE']._serialized_start=278
  _globals['_RESPONSE']._serialized_end=556
# @@protoc_insertion_point(module_scope)

def create(isSuccess=None, message=None):
  return Result(isSuccess=isSuccess, message=message)