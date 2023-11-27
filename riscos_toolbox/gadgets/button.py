"""RISC OS Toolbox - Gadgets - Button"""

from . import Gadget, GadgetDefinition

import swi
import ctypes


class Button(Gadget):
    _type = 960

    GetFlags       = _type + 0
    SetFlags       = _type + 1
    SetValue       = _type + 2
    GetValue       = _type + 3
    SetValidation  = _type + 4
    GetValidation  = _type + 5
    SetFont        = _type + 6

    # Properties
    @property
    def icon_flags(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiIi;I',
                       0, self.window.id, Button.GetFlags, self.id)

    @icon_flags.setter
    def icon_flags(self, flags):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIiII',
                0, self.window.id, Button.SetFlags, self.id, 0, flags)

    @property
    def value(self):
        return self._miscop_get_string(Button.GetValue)

    @value.setter
    def value(self, value):
        return self._miscop_set_string(Button.SetValue, value)

    @property
    def validation(self):
        return self._miscop_get_string(Button.GetValidation)

    @validation.setter
    def validation(self, validation):
        return self._miscop_set_string(Button.SetValidation, validation)

    # Methods
    def set_font(self, *args, **kwargs):
        self._miscop_set_font(Button.SetFont, *args, **kwargs)


class ButtonDefinition(GadgetDefinition):
    _fields_ = [
        ("button_flags", ctypes.c_int32),
        ("value", ctypes.c_char_p),
        ("max_value", ctypes.c_int32),
        ("validation", ctypes.c_char_p),
        ("max_validation", ctypes.c_int32)
    ]

    Button_TaskSpriteArea  = 0x00000001
    Button_AllowMenuClicks = 0x00000002
