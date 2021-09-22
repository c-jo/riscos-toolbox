"""RISC OS Toolbox - Gadgets - Button"""

from . import Gadget, create, encode_and_len
from swi import swi
import ctypes

class ActionButton(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x82881: # ActionButton_Selected
            self.window.actionbutton_selected(self)

class Button(Gadget):
    class Block(ctypes.Structure):
        _anonymous_ = ("header",)
        _fields_ = [("header",         Gadget.Header  ),
                    ("button_flags",   ctypes.c_uint  ),
                    ("value",          ctypes.c_char_p),
                    ("max_value",      ctypes.c_uint  ),
                    ("validation",     ctypes.c_char_p),
                    ("max_validation", ctypes.c_uint  )]

    def __init__(self, window, id):
        super().__init__(window, id)

    def set_font(self, font, width, height=None):
        if height==None:
            height=width
        swi('Toolbox_ObjectMiscOp','0IiIsII',
            self.window.id,966,self.id,font,int(width*16), int(height*16))

    def create(window, box, button_flags,
               value=None, max_value=None,
               validation=None, max_validation=None):
         block = Button.Block()
         block.button_flags = button_flags
         block.value, block.max_value = encode_and_len(value, max_value)
         block.validation, block.max_validation = encode_and_len(validation, max_validation)
         return Button(window, create(window, block, 960, box))

class Draggable(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

        if event_code == 0x82887: # Draggable_DragStarted
            self.window.draggable_dragstarted(self)

        if event_code == 0x82888: # Draggable_DragEnded
            self.window.draggable_dragended(self,
                            poll_block[4],poll_block[5],   # window, icon
                            (poll_block[6],poll_block[7])) # mouse pos (x,y)

class Label(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

class LabelledBox(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

class NumberRange(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x8288d: # NumberRange_ValueChanged
            self.window.numberrange_valuechanged(self,
                poll_block[4]) # new value

class OptionButton(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    @property
    def selected(self):
        return bool(
            swi('Toolbox_ObjectMiscOp','0III;I',self.window.id,197,self.id))

    @selected.setter
    def selected(self, value):
        swi('Toolbox_ObjectMiscOp','0IIII',self.window.id,196,self.id,value)

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

class ScrollList(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def get_state(self):
        return swi('Toolbox_ObjectMiscOp','0II;I',
                   self.window.id, 16410, self.id)

    def set_state(self, state):
        return swi('Toolbox_ObjectMiscOp','0III',
                   self.window.id, 16411, self.id, state)

    def add_item(self, text, index):
        swi('Toolbox_ObjectMiscOp','0IIIs00I',
            self.window.id, 16412, self.id, text, index)

    def delete_items(self, start, end):
        swi('Toolbox_ObjectMiscOp','0IIIII',
            self.window.id, 16413, self.id, start, end)

    def get_selected(self, offset=-1):
        return swi('Toolbox_ObjectMiscOp','0IIIi;i',
                    self.window.id, 16416, self.id, offset)

    def make_visible(self, index):
        swi('Toolbox_ObjectMiscOp','0III',
            self.window.id, 16417, self.id, index)


    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x140181: # ScrollList_Selection
            self.window.scrolllist_selection(self,
                            poll_block[4],poll_block[5]) # flags, item

class Slider(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x82886: # Slider_ValueChanged
            self.window.slider_valuechanged(self,
                            poll_block[4]) # new value

class StringSet(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x8288f: # StringSet_AboutToBeShown
            self.window.stringset_abouttobeshown(self)

        if event_code == 0x8288e: # StringSet_ValueChanged
            self.window.stringset_valuechanged(self,
                        poll_block.nullstring(16, poll_block[0])) # new string

class TextArea(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

class ToolAction(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)
      
class WritableField(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x82885: # WritableField_ValueChanged:
            self.window.writablefield_valuechanged(self,
                        poll_block.nullstring(16, poll_block[0])) # new string
