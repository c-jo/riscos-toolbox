"""RISC OS Toolbox - ColourDBox"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
from enum import Enum
import swi
import ctypes


class Colour(object):
    def Colour(self, blue, green, red):
        self.blue = int(blue)
        self.green = int(green)
        self.red = int(red)


ColourModel = Enum("ColourModel", ["RGB", "CMYK", "HSV"], start=0)


class ColourDbox(Object):
    class_id = 0x829c0
    # Methods
    GetWimpHandle     = 0
    GetDialogueHandle = 1
    SetColour         = 2
    GetColour         = 3
    SetColourModel    = 4
    GetColourModel    = 5
    SetNoneAvailable  = 6
    GetNoneAvailable  = 7
    # Events
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    ColourSelected    = class_id + 2

    @property
    def get_wimp_handle(self):
        return self._miscop_get_signed(ColourDbox.GetWimpHandle)

    @property
    def get_dialogue_handle(self):
        return self._miscop_get_unsigned(ColourDbox.GetDialogueHandle)

    @property
    def colour(self):
        colour_block = swi.block[6]
        swi.swi('Toolbox_ObjectMiscOp', 'IIII',
                0, self.id, ColourDbox.GetColour, colour_block, 24)
        return Colour(colour_block[1], colour_block[2], colour_block[3])

    @colour.setter
    def colour(self, colour):
        if colour is None:
            swi.swi('Toolbox_ObjectMiscOp', 'III0',
                    ColourDbox.SelectNone, self.id, ColourDbox.SetColour)
        else:
            colour_block = swi.block[6]
            colour_block[0] = 0  # Must be zero
            colour_block[1] = colour.blue
            colour_block[2] = colour.green
            colour_block[3] = colour.red
            colour_block[4] = 0  # No extra data
            colour_block[5] = 0
            swi.swi('Toolbox_ObjectMiscOp', 'IIIb',
                    0, self.id, ColourDbox.SetColour, colour_block)

    @property
    def colour_model(self):
        colour_block = swi.block[6]
        swi.swi('Toolbox_ObjectMiscOp', 'IIII',
                0, self.id, ColourDbox.GetColour, colour_block, 24)
        return ColourModel(colour_block[5])

    @colour_model.setter
    def colour_model(self, colour_model):
        colour_block = swi.block[6]
        colour_block[0] = 0  # Must be zero
        colour_block[1] = 0
        colour_block[2] = 0
        colour_block[3] = 0
        colour_block[4] = 0  # No extra data
        colour_block[5] = colour_model
        swi.swi('Toolbox_ObjectMiscOp', 'IIIb', 0,
                self.id, ColourDbox.SetColourModel, colour_block)

    @property
    def none_available(self):
        return self._miscop_get_signed(ColourDbox.GetNoneAvailable) != 0

    @none_available.setter
    def none_available(self, available):
        self._miscop_set_signed(
            ColourDbox.SetNoneAvailable, 1 if available else 0)


# ColourDboxEvents
class ColourDboxAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = ColourDbox.AboutToBeShown


class ColourDboxDialogueCompletedEvent(ToolboxEvent):
    event_id = ColourDbox.DialogueCompleted


class ColourDboxColourSelectedEvent(ToolboxEvent):
    event_id = ColourDbox.ColourSelected
    _fields_ = [("_colour_data", ctypes.c_int32 * 4)]

    @property
    def model(self):
        return ColourModel(self._colour_data[0])

    @property
    def red(self):
        return self._colour_data[1]

    @property
    def green(self):
        return self._colour_data[2]

    @property
    def blue(self):
        return self._colour_data[3]
