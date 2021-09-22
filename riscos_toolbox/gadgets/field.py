from . import Gadget
from swi import swi

class DisplayField(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def set_text(self, text):
        swi('Toolbox_ObjectMiscOp','0IiIs',
            self.window.id,448,self.id,text)

    def set_font(self, font, width, height=None):
        if height==None:
            height=width
        swi('Toolbox_ObjectMiscOp','0IiIsII',
            self.window.id,450,self.id,
            font,int(width*16), int(height*16))

class WritableField(Gadget):
    def __init__(self, window, id):
        super().__init__(window, id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x82885: # WritableField_ValueChanged:
            self.window.writablefield_valuechanged(self,
                        poll_block.nullstring(16, poll_block[0])) # new string
