"""RISC OS Toolbox - ColourMenu"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
from enum import Enum
import ctypes


class ColourMenu(Object):
    class_id = 0x82980
    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1
    Selection      = class_id + 2

    Colour = Enum(
        "Colour",
        "White Grey1 Grey2 Grey3 Grey4 Grey5 Grey6 Black "
        "DarkBlue Yellow Green Red Cream ArmyGreen Orange LightBlue "
        "None".split())

    NoSelection = None

    @property
    def colour(self):
        colour = self._miscop_get_signed(1)
        return colour if colour > 0 else None

    @colour.setter
    def colour(self, colour):
        self._miscop_set_signed(0, colour if colour else -1)

    @property
    def none_available(self):
        return self._miscop_get_unsigned(3) != 0

    @none_available.setter
    def none_available(self, available):
        self._miscop_set_unsigned(2, 1 if available else 0)

    @property
    def title(self):
        return self._miscop_get_string(5)

    @title.setter
    def title(self, title):
        self._miscop_set_string(4, title)


# ColourMenu Events
class ColourMenuAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = ColourMenu.AboutToBeShown


class ColourMenuHasBeenHiddenEvent(ToolboxEvent):
    event_id = ColourMenu.HasBeenHidden


class ColourMenuSelectionEvent(ToolboxEvent):
    event_id = ColourMenu.Selection
    _fields_ = [("_selection", ctypes.c_int32)]

    @property
    def selection(self):
        return self.selection if self.selection != -1 else None
