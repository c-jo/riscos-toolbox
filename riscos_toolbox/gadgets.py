"""RISC OS Toolbox - Gadgets"""

from swi import swi

class Gadget:
    def __init__(self, window, id):
        self.window = window
        self.id     = id

        window.gadgets[id] = self

    def get_flags(self):
        """Gets the gadgets flags."""
        return swi('Toolbox_ObjectMiscOp','0III;I',self.window.id,64,self.id)

    def set_flags(self, flags):
        """Sets the gadgets flags."""
        swi('Toolbox_ObjectMiscOp','0IIII',self.window.id,65,self.id,flags)

    def get_flag(self, flag):
        """Gets one gadget flag."""
        return self.get_flags() & 1<<flag != 0

    def set_flag(self, flag, value):
        """Sets one gadget flag."""
        mask = 0xffffff - 1<<flag
        self.set_flags(
            self.get_flags() & mask | (1<<flag if value else 0))

    def event_handler(self, event_code, id_block, poll_block):
        pass
        #raise(RuntimeError(f'toolbox event 0x{event_code:x} not handled.'))

    @property
    def faded(self):
        return self.get_flag(31)

    @faded.setter
    def faded(self, value):
        self.set_flag(31, value)

class ActionButton(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x82881: # ActionButton_Selected
            self.window.actionbutton_selected(self)

class Adjuster(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x8288c: # Adjuster_Clicked
            self.window.adjuster_clicked(
                            self, poll_block[4])

class Button(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

class DisplayField(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def set_text(self, text):
        swi('Toolbox_ObjectMiscOp','0IIIs',self.window.id,448,self.id,text)

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
                            poll_block.nullstring(poll_bllock+16,size))
