"""RISC OS Toolbox - FontDbox"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
import ctypes
import swi


class FontDbox(Object):
    class_id = 0x82a00
    # Methods
    GetWindowId  = 0
    SetFont      = 1
    GetFont      = 2
    SetSize      = 3
    GetSize      = 4
    SetTryString = 5
    GetTryString = 6
    SetTitle     = 7
    GetTitle     = 8
    # Events
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    ApplyFont         = class_id + 2

    # Constants
    SetSize_Height = 1
    SetSize_Aspect = 2

    @property
    def window_id(self):
        return self._miscop_get_signed(FontDbox.GetWindowId)

    @property
    def font(self):
        return self._miscop_get_string(FontDbox.GetFont)

    @font.setter
    def font(self, font):
        self._miscop_set_string(FontDbox.SetFont, font)

    @property
    def size(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiI;i.',
                       0, self.id, FontDbox.GetSize)

    @size.setter
    def size(self, size):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIi0',
                FontDbox.SetSize_Height, self.id, FontDbox.SetSize, size)

    @property
    def aspect(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiI;.i',
                       0 self.id, FontDbox.GetSize)

    @aspect.setter
    def aspect(self, aspect):
        swi.swi('Toolbox_ObjectMiscOp', 'IiI0i',
                FontDbox.SetSize_Aspect, self.id, FontDbox.SetSize, aspect)

    @property
    def try_string(self):
        return self._miscop_get_string(FontDbox.GetTryString)

    @try_string.setter
    def try_string(self, try_string):
        self._miscop_set_string(FontDbox.SetTryString, try_string)

    @property
    def title(self):
        return self._miscop_get_string(FontDbox.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(FontDbox.SetTitle, title)


# FontDbox Events
class FontDboxAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = FontDbox.AboutToBeShown

class FontDboxApplyFontEvent(ToolboxEvent):
    event_id = FontDbox.ApplyFont
    _fields_ = [
        ('height', ctypes.c_int32),
        ('aspect', ctypes.c_int32),
        ('_font', ctypes.c_char * 208),
    ]

    @property
    def font(self):
        return self._font.decode('latin-1')


class FontDboxDialogueCompletedEvent(ToolboxEvent):
    event_id = FontDbox.DialogueCompleted
