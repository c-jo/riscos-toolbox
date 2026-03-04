from ..events import UserMessage
from .. import Point

import ctypes


class Messages:
    DataSave = 1
    DataSaveAck = 2
    DataLoad = 3
    DataLoadAck = 4
    DataOpen = 5
    RAMFetch = 6
    RAMTransmit = 7
    DataSaved = 0x0d


class DataTransferMessage(UserMessage):
    _fields_ = [
        ("destination_window", ctypes.c_int32),
        ("destination_icon", ctypes.c_int32),
        ("destination_position", Point),
        ("estimated_size", ctypes.c_int32),
        ("file_type", ctypes.c_int32),
        ("_leaf_name", ctypes.c_char * 212),
    ]

    @property
    def leaf_name(self):
        return self._leaf_name.decode('latin-1')

    @leaf_name.setter
    def leaf_name(self, value):
        name = bytes(value, encoding='latin-1')
        if len(name) > 211:
            raise ValueError("File name too long")
        self._leaf_name = name + b"\x00"
        self.size = (44 + len(name) + 4) & ~3


class DataSaveMessage(DataTransferMessage):
    event_id = Messages.DataSave


class DataSaveAckMessage(DataTransferMessage):
    event_id = Messages.DataSaveAck


class DataLoadMessage(DataTransferMessage):
    event_id = Messages.DataLoad


class DataLoadAckMessage(DataTransferMessage):
    event_id = Messages.DataLoadAck


class DataSavedMessage(UserMessage):
    event_id = Messages.DataSaved


class DataOpenMessage(UserMessage):
    event_id = Messages.DataOpen

    _fields_ = [
        ("window_handle", ctypes.c_int32),
        ("spare", ctypes.c_int32),
        ("position", Point),
        ("zero", ctypes.c_int32),
        ("file_type", ctypes.c_int32),
        ("_path_name", ctypes.c_char * 212),
    ]

    @property
    def path_name(self):
        return self._path_name.decode('latin-1')


class RAMFetchMessage(UserMessage):
    event_id = Messages.RAMFetch
    _fields_ = [
        ("buffer", ctypes.c_void_p),
        ("size", ctypes.c_int32),
    ]


class RAMTransmitMessage(UserMessage):
    event_id = Messages.RAMTransmit
    _fields_ = [
        ("buffer", ctypes.c_void_p),
        ("count", ctypes.c_int32),
    ]
