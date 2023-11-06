"""RISC OS Toolbox - FontDbox"""

from ..events import AboutToBeShownEvent, ToolboxEvent
import ctypes
import swi


class FontDbox(object):
    class_id = 0x82a00
    AboutToBeShown    = class_id + 0
    ApplyFont         = class_id + 1
    DialogueCompleted = class_id + 2

    @property
    def window_id(self):
        return self._miscop_get_signed(0)

    @property
    def font(self):
        return self._miscop_get_string(2)

    @font.setter
    def font(self, title):
        self._miscop_set_string(1, title)

    @property
    def size(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0II;ii', self.id, 4)

    @size.setter
    def size(self, height, ratio):
        swi.swi('Toolbox_ObjectMiscOp', '0IIii',
                self.id, 3, height, ratio)

    @property
    def try_string(self):
        return self._miscop_get_string(6)

    @try_string.setter
    def try_string(self, try_string):
        self._miscop_set_string(5, try_string)

    @property
    def title(self):
        return self._miscop_get_string(8)

    @title.setter
    def title(self, title):
        self._miscop_get_string(7, title)


# FontDbox Events
class FontDboxAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = FontDbox.AboutToBeShown


class FontDboxApplyFontEvent(ToolboxEvent):
    event_id = FontDbox.ApplyFont


class FontDboxDialogueCompletedEvent(ToolboxEvent):
    event_id = FontDbox.DialogueCompleted
    _fields_ = [
        ('height', ctypes.c_int32),
        ('aspect', ctypes.c_int32),
        ('_font', ctypes.c_char * 208),
    ]

    @property
    def font(self):
        return self._font.decode('latin-1')
