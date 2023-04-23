from ..base import Object
from ..events import ToolboxEvent

import swi
import ctypes

class SaveAs(Object):
    class_id = 0x82bc0

    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    SaveToFile        = class_id + 2
    FillBuffer        = class_id + 3
    SaveCompleted     = class_id + 4

    @property
    def window_id(self):
        return self._miscop_get_unsigned(0)

    @property
    def title(self):
        return self._miscop_get_string(2)

    @title.setter
    def title(self, title):
        self._miscop_set_string(1, title)

    @property
    def file_name(self):
        return self._miscop_get_string(4)

    @file_name.setter
    def file_name(self, file_name):
        self._miscop_set_string(3, file_name)

    @property
    def file_type(self):
        return self._miscop_get_unsigned(6)

    @file_type.setter
    def file_type(self, file_type):
        self._miscop_set_unsigned(5, file_type)

    @property
    def file_size(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0II;I', self.id, 8)

    @file_size.setter
    def file_size(self, file_size):
        swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.id, 7, file_size)

    def selection_available(self, available):
        swi.swi('Toolbox_ObjectMiscOp', '0III', self.id, 9, available)

    def set_data_addresss(self, address, size, sel_addr, sel_size):
        swi.swi('Toolbox_ObjectMiscOp', '0IIIIII', self.id, 10,
                address, size, sel_addr, sel_size)

    def buffer_filled(self, buffer, bytes_written):
        swi.swi('Toolbox_ObjectMiscOp', '0IIII', self.id, 11,
                buffer, bytes_written)

    def file_save_completed(self, filename, saved=True):
        swi.swi('Toolbox_ObjectMiscOp', 'IIIs',
                1 if saved else 0, self.id, 12, filename)

class SaveToFileEvent(ToolboxEvent):
    event_id = SaveAs.SaveToFile
    _fields_ = [ ("wimp_message_no", ctypes.c_int32),
                 ("filename", ctypes.c_char*208) ]

    @property
    def selection(self):
        return True if (self.flags & 1<<0) else False

class FillBufferEvent(ToolboxEvent):
    event_id = SaveAs.FillBuffer
    _fields_ = [ ("size", ctypes.c_uint32),
                 ("address", ctypes.c_void_p),
                 ("no_bytes", ctypes.c_uint32) ]

class SaveCompletedEvent(ToolboxEvent):
    event_id = SaveAs.SaveCompleted
    _fields_ = [ ("filename", ctypes.c_char*212) ]
