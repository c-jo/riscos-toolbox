from . import Gadget

class DisplayField(Gadget):
    _type = 448

    @property
    def value(self):
        return self._miscop_get_text(449)

    @value.setter
    def value(self, value):
        self._miscop_set_text(448, value)
