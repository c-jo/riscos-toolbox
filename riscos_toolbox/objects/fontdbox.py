"""RISC OS Toolbox - FontDBox"""

from ..base import Object
import swi

class FontDBox(object):
    class_id = 0x82a00
    AboutToBeShown    = class_id + 0
    ApplyFont         = class_id + 1
    DialogueCompleted = class_id + 2

    @property
    def window_id(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 0)

    @property
    def font(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 2)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 2, buf, buf_size)
        return buf.nullstring()

    @font.setter
    def font(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 1, title)

    @property
    def size(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0II;II', self.id, 4)

    @size.setter
    def size(self, height, ratio):
        return swi.swi('Toolbox_ObjectMiscOp', '0III',
                       self.id, 3, height, ratio)

    @property
    def try_string(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 6)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 6, buf, buf_size)
        return buf.nullstring()

    @try_string.setter
    def try_sting(self, try_string):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 5, try_string)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 8)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 8, buf, buf_size)
        return buf.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 7, title)
