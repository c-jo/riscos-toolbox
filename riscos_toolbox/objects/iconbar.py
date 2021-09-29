"""RISC OS Toolbox - Iconbar"""

from .. import Object

class Iconbar(Object):
    class_id = 0x82900
    def __init__(self, id):
        super().__init__(id)

    def event_handler(self, event_code, id_block, poll_block):
        flags = poll_block.tounsigned(3)
        if event_code == 0x82900: # Iconbar_Clicked
            self.clicked(id_block, flags == 0x01)
        if event_code == 0x82901: # Iconbar_SelectAboutToBeShown
            self.select_about_to_be_shown(id_block)
        if event_code == 0x82902: # Iconbar_AdjustAboutToBeShown
            self.adjust_about_to_be_shown(id_block)

    def clicked(self, id_block, adjust):
        pass

    def select_about_to_be_shown(self, id_block):
        pass

    def adjust_about_to_be_shown(self, id_block):
        pass
