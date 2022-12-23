"""RISC OS Toolbox - Scale"""

from ..base import Object
from ..events import EventDecoder

class Scale(Object):
    class_id = 0x82c00

    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    ApplyFactor       = class_id + 2

    @EventDecoder(ApplyFactor)
    def decode_apply_factor(poll_block):
        return (poll_block[4],)

    def __init__(self, id):
        super().__init__(id)

    @property
    def window_id(self):
        return swi.swi("Toolbox_ObjectMiscOp","0II;.I",self.id, 0)

    @property
    def value(self):
        return swi.swi("Toolbox_ObjectMiscOp","0II;I",self.id, 2)

    @value.setter
    def value(self, value):
        return swi.swi("Toolbox_ObjectMiscOp","0III",self.id, 1, value)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 6)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI',
                self.id, 6, buf, buf_size)
        return buf.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 5, title)

    def event_handler_old(self, event_code, id_block, poll_block):
        if event_code == Scale.class_id+ 0: #AboutToBeShown
            return self.about_to_be_shown(id_block)
        if event_code == Scale.class_id+ 1: # Scale_DialogueCompleted
            return self.dialogue_completed(id_block)
        if event_code == Scale.class_id+ 2: # Scale_Applyfactor
            return self.apply_factor(id_block, poll_block[4])
            return False

    def about_to_be_shown(self, id_block):
        return False

    def apply_factor(self, id_block, factor):
        return False

    def dialogue_completed(self, id_block):
        return False
