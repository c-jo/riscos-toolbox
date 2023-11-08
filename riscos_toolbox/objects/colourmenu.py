"""RISC OS Toolbox - ColourMenu"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
from enum import Enum
import ctypes
Colour = Enum(
    "Colour",
    "NoSelection "
    "White Grey1 Grey2 Grey3 Grey4 Grey5 Grey6 Black "
    "DarkBlue Yellow Green Red Cream ArmyGreen Orange LightBlue "
    "NONE".split(), start=-1)


class ColourMenu(Object):
    class_id = 0x82980
    # Methods
    SetColour        = 0
    GetColour        = 1
    SetNoneAvailable = 2
    GetNoneAvailable = 3
    SetTitle         = 4
    GetTitle         = 5
    # Events
    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1
    Selection      = class_id + 2

    @property
    def colour(self):
        colour = self._miscop_get_signed(1)
        return Colour(colour) if 0 <= colour <= 16 else Colour.NoSelection

    @colour.setter
    def colour(self, colour):
        self._miscop_set_signed(0, Colour(colour))

    @property
    def none_available(self):
        return self._miscop_get_unsigned(ColourMenu.GetNoneAvailable) != 0

    @none_available.setter
    def none_available(self, available):
        self._miscop_set_unsigned(ColourMenu.SetNoneAvailable, 1 if available else 0)

    @property
    def title(self):
        return self._miscop_get_string(ColourMenu.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(ColourMenu.SetTitle, title)


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
        return Colour(self.selection)
