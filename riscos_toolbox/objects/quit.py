"""RISC OS Toolbox - Quit"""

from .. import Object
import swi

class Quit(Object):
    class_id = 0x82a90
    AboutToBeShown    = class_id + 0
    Quit              = class_id + 1
    DialogueCompleted = class_id + 2
    Cancel            = class_id + 3

    def __init__(self, id):
        super().__init__(id)

    @property
    window_id(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 0)

    @property
    def message(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 2)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 2, buf, buf_size)
        return buf.nullstring()

    @message.setter
    def message(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 1, title)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 4)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 4, buf, buf_size)
        return buf.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 3, title)