from ..base import Object
from ..events import ToolboxEvent, AboutToBeShownEvent

import swi
import ctypes


class SaveAs(Object):
    class_id = 0x82bc0
    # Methods
    GetWindowId        = 0
    SetTitle           = 1
    GetTitle           = 2
    SetFileName        = 3
    GetFileName        = 4
    SetFileType        = 5
    GetFileType        = 6
    SetFileSize        = 7
    GetFileSize        = 8
    SelectionAvailable = 9
    SetDataAddress     = 10
    BufferFilled       = 11
    FileSaveCompleted  = 12
    # Events
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    SaveToFile        = class_id + 2
    FillBuffer        = class_id + 3
    SaveCompleted     = class_id + 4
    # Constants
    Directory           = 0x1000
    Application         = 0x2000
    OnlySaveSelection   = 0x00000001
    SuccessfulSave      = 0x00000001
    SelectionBeingSaved = 0x00000001
    SelectionSaved      = 0x00000001
    DestinationSafe     = 0x00000002

    @property
    def window_id(self):
        return self._miscop_get_unsigned(SaveAs.GetWindowId)

    @property
    def title(self):
        return self._miscop_get_string(SaveAs.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(SaveAs.SetTitle, title)

    @property
    def file_name(self):
        return self._miscop_get_string(SaveAs.GetFileName)

    @file_name.setter
    def file_name(self, file_name):
        self._miscop_set_string(SaveAs.SetFileName, file_name)

    @property
    def file_type(self):
        return self._miscop_get_unsigned(SaveAs.GetFileType)

    @file_type.setter
    def file_type(self, file_type):
        self._miscop_set_unsigned(SaveAs.SetFileType, file_type)

    @property
    def file_size(self):
        return self._miscop_get_unsigned(SaveAs.GetFileSize)

    @file_size.setter
    def file_size(self, file_size):
        self._miscop_set_signed(SaveAs.SetFileSize, file_size)

    def selection_available(self, available):
        self._miscop_set_unsigned(SaveAs.SelectionAvailable, 1 if available else 0)

    def set_data_address(self, address, size, sel_addr=0, sel_size=0):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIIIII',
                0, self.id, SaveAs.SetDataAddress,
                address, size, sel_addr, sel_size)

    def buffer_filled(self, buffer, bytes_written):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIII',
                0, self.id, SaveAs.BufferFilled,
                buffer, bytes_written)

    def file_save_completed(self, filename, saved=True):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIs',
                1 if saved else 0, self.id, SaveAs.FileSaveCompleted, filename)


class SaveAsAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = SaveAs.AboutToBeShown


class SaveAsDialogueCompletedEvent(ToolboxEvent):
    event_id = SaveAs.DialogueCompleted


class SaveAsSaveToFileEvent(ToolboxEvent):
    event_id = SaveAs.SaveToFile
    _fields_ = [
        ("filename", ctypes.c_char * 212),
    ]

    @property
    def selection(self):
        return True if (self.flags & SaveAs.SelectionBeingSaved) else False


class FillBufferEvent(ToolboxEvent):
    event_id = SaveAs.FillBuffer
    _fields_ = [
        ("size", ctypes.c_uint32),
        ("address", ctypes.c_void_p),
        ("no_bytes", ctypes.c_uint32),
    ]

    @property
    def selection_being_saved(self):
        return True if (self.flags & SaveAs.SelectionBeingSaved) else False


class SaveAsSaveCompletedEvent(ToolboxEvent):
    event_id = SaveAs.SaveCompleted
    _fields_ = [
        ("wimp_message_no", ctypes.c_int32),
        ("filename", ctypes.c_char * 208),
    ]

    @property
    def selection_saved(self):
        return True if (self.flags & SaveAs.SelectionSaved) else False

    @property
    def destination_safe(self):
        return True if (self.flags & SaveAs.DestinationSafe) else False


# For compatability with 1.0.2 and below
AboutToBeShownEvent = SaveAsAboutToBeShownEvent
SaveToFileEvent = SaveAsSaveToFileEvent
SaveCompletedEvent = SaveAsSaveCompletedEvent
