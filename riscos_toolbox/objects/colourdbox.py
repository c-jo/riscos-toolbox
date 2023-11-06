"""RISC OS Toolbox - ColourDBox"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
from enum import Enum
import ctypes


class ColourDbox(Object):
    class_id = 0x829c0
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    ColourSelected    = class_id + 2

    ColourModel = Enum("ColourModel", ["RGB", "CMYK", "HSV"], start=0)

    @property
    def colour(self):
        colour = self._miscop_get_signed(1)
        return colour if colour > 0 else None

    @colour.setter
    def colour(self, colour):
        self._miscop_set_signed(0, colour if colour else -1)

    @property
    def none_available(self):
        return self._miscop_get_signed(3) != 0

    @none_available.setter
    def none_available(self, available):
        self._miscop_set_signed(2, 1 if available else 0)

    @property
    def title(self):
        return self._miscop_get_string(5)

    @title.setter
    def title(self, title):
        self._miscop_set_string(4, title)


# ColourDboxEvents
class ColourDboxAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = ColourDbox.AboutToBeShown


class ColourDboxDialogueCompletedEvent(ToolboxEvent):
    event_id = ColourDbox.DialogueCompleted


class ColourDboxColourSelectedEvent(ToolboxEvent):
    event_id = ColourDbox.ColourSelected
    _fields_ = [("_colour_data", ctypes.c_int32 * 53)]

    @property
    def model(self):
        return ColourModel(_colour_data[0])

    @property
    def red(self):
        return _colour_data[1]

    @property
    def green(self):
        return _colour_data[2]

    @property
    def blue(self):
        return _colour_data[3]
