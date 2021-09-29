"""RISC OS Toolbox - Gadgets - Button"""

from . import Gadget, encode_and_len
import swi
import ctypes

class ActionButton(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    @property
    def text(self):
        return self._miscop_get_text(129)

    @text.setter
    def text(self, text):
        self._miscop_set_text(128, text)

    @property
    def event(self):
        return self._miscop_get_int(131)

    @event.setter
    def event(self, ev):
        return self._miscop_get_int(130, ev)

    @property
    def click_show(self):
        return self._miscop_get_int(133)

    @click_show.setter
    def click_show(self, cs):
        return self._miscop_get_int(132, cs)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x82881: # ActionButton_Selected
            self.window.actionbutton_selected(id_block, self)

class Button(Gadget):
    class Definition(ctypes.Structure):
        _anonymous_ = ("header",)
        _fields_ = [("header",         Gadget.Header  ),
                    ("button_flags",   ctypes.c_uint  ),
                    ("value",          ctypes.c_char_p),
                    ("max_value",      ctypes.c_uint  ),
                    ("validation",     ctypes.c_char_p),
                    ("max_validation", ctypes.c_uint  )]

        def __init__(self, box, button_flags,
                           help_message=None, max_help=None,
                           value=None, max_value=None,
                           validation=None, max_validation=None):
            Gadget.Header.__init__(self, flags=0, type=960, box=box, help_message=help_message, max_help=max_help)
            self.button_flags = button_flags
            self.value, self.max_value = encode_and_len(value, max_value)
            self.validation, self.max_validation = encode_and_len(validation, max_validation)

        def create(self, window):
            return window.add_gadget(ctypes.addressof(self), Button)

    def __init__(self, window, id):
        super().__init__(window, id)

    @property
    def flags(self):
        return swi.swi('Toolbox_ObjectMiscOp','0III;I',
                        self.window.id, 960, self.id)

    @flags.setter
    def flags(self, flags):
        swi.swi('Toolbox_ObjectMiscOp','0III0I',
                 self.window.id, 961, self.id, flags)

    @property
    def value(self):
        return self._miscop_get_text(963)

    @value.setter
    def value(self, value):
        return self._miscop_set_text(962, value)

    @property
    def validation(self):
        return self._miscop_get_text(965)

    @validation.setter
    def validation(self, validation):
        return self._miscop_set_text(964, validation)

    def font(self, font, width, height=None):
        if height is None:
            height=width
        swi.swi('Toolbox_ObjectMiscOp','0IIIsII',
            self.window.id, 966, self.id, font, int(width*16), int(height*16))

class OptionButton(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    @property
    def selected(self):
        return bool(
            swi.swi('Toolbox_ObjectMiscOp','0III;I',self.window.id,197,self.id))

    @selected.setter
    def selected(self, value):
        swi.swi('Toolbox_ObjectMiscOp','0IIII',self.window.id,196,self.id,value)

class PopupMenu(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x8288b: # Popup_AboutToBeShown
            self.window.popup_abouttobeshown(self,
                poll_block[4],poll_block[5],   # menu_id, show_type
                (poll_block[6],poll_block[7])) # top left (x,y)

class RadioButton(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x82883: # RadioButton_StateChanged
            self.window.radiobutton_statechanged(self,
                            poll_block[4], poll_block[5]) # state, old_on
