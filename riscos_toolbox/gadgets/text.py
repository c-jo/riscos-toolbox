from . import Gadget
from swi import swi

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
