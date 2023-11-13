from . import Gadget


class DisplayField(Gadget):
    _type = 448
    SetValue = _type + 0
    GetValue = _type + 1
    SetFont = _type + 2

    # Flags
    LeftJustified = 0
    RightJustified = 1
    Centered = 2

    # Properties
    @property
    def value(self):
        return self._miscop_get_text(DisplayField.GetValue)

    @value.setter
    def value(self, value):
        self._miscop_set_string(DisplayField.SetValue, value)

    # Methods
    def set_font(self, *args, **kwargs):
        self._miscop_set_font(DisplayField.SetFont, *args, **kwargs)
