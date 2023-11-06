"""RISC OS Toolbox - FontDBox"""

from ..events import AboutToBeShownEvent, ToolboxEvent
import ctypes


class FontMenu(object):
    class_id = 0x82a40
    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1
    Selection      = class_id + 2

    @property
    def font(self):
        return self._miscop_get_string(1)

    @font.setter
    def font(self, font):
        self._miscop_set_string(0, font)


# FontMenu Events
class FontMenuAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = FontMenu.AboutToBeShown


class FontMenuHasBeenHiddenEvent(ToolboxEvent):
    event_id = FontMenu.HasBeenHidden


class FontMenuSelectionEvent(ToolboxEvent):
    event_id = FontMenu.Selection
    _fields_ = [('_font_id', ctypes.c_char * 216)]

    @property
    def font_id(self):
        return self._font_id.decode('latin-1')
