"""RISC OS Toolbox - FontDBox"""

from .. import Object
import swi

class FontMenu(object):
    class_id = 0x82a40
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    Selection         = class_id + 2

    def __init__(self, id):
        super().__init__(id)

    @property
    def font(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 1)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 1, buf, buf_size)
        return buf.nullstring()

    @font.setter
    def font(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 0, title)
