from . import Gadget, GadgetDefinition
from .. import ComponentID
from ..events import ToolboxEvent
import ctypes


class WritableField(Gadget):
    _type = 512

    # Methods
    SetValue     = _type + 0
    GetValue     = _type + 1
    SetAllowable = _type + 2
    GetAllowable = _type + 3
    SetFont      = _type + 4
    GetFont      = _type + 5

    # Events
    ValueChanged = 0x82885  # Window_SWIChunkBase (0x82880) + 5

    # Flags
    GenerateUserValueChanged = 0x00000001
    GenerateSetValueChanged  = 0x00000002
    LeftJustify              = 0x00000000
    RightJustify             = 0x00000004
    Centred                  = 0x00000008
    Justification            = 0x0000000C
    Password                 = 0x00000010

    # Properties
    @property
    def value(self):
        return self._miscop_get_string(WritableField.GetValue)

    @value.setter
    def value(self, value):
        return self._miscop_set_string(WritableField.SetValue, value)

    @property
    def allowable(self):
        return self._miscop_get_string(WritableField.GetAllowable)

    @allowable.setter
    def allowable(self, allowable):
        return self._miscop_set_string(WritableField.SetAllowable, allowable)

    # Methods
    def set_font(self, *args, **kwargs):
        self._miscop_set_font(WritableField.SetFont, *args, **kwargs)


class WritableFieldDefinition(GadgetDefinition):
    _gadget_class = WritableField

    _fields_ = [
        ("text", ctypes.c_char_p),
        ("max_text_len", ctypes.c_int32),
        ("allowable", ctypes.c_char_p),
        ("max_allowable_len", ctypes.c_int32),
        ("before", ComponentID),
        ("after", ComponentID),
    ]


class WritableFieldValueChangedEvent(ToolboxEvent):
    event_id = WritableField.ValueChanged

    _fields_ = [("_string", ctypes.c_char * 240)]

    @property
    def string(self):
        return self._string.decode('latin-1')
