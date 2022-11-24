"""RISC OS Toolbox - PrintDBox"""

from .. import Object
from enum import Enum
from collections import namedtuple

class ColourDboxr(Object):
    class_id = 0x82b00
    AboutToBeShown      = class_id + 0
    DialogueCompleted   = class_id + 1
    SetupAboutToBeShown = class_id + 2
    Save                = class_id + 3
    Setup               = class_id + 4
    Print               = class_id + 5

    Orientation = Enum("Orientation", ["Sideways", "Upright"])
    PageRange   = namedtuple("PageRange", ["Start", "End"])


    def __init__(self, id):
        super().__init__(id)

    @property
    window_id(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;i", 0,self.id, 0)

    @property
    page_ranfe(self):
        return PageRange(swi.swi(
            "Toolbox_ObjectMiscOp","III;II", 0, self.id, 2))

    @page_range.setter
    page_ranger(self, page_range):
        swi.swi("Toolbox_ObjectMiscOp","IIIII",
                0, self.id, 1, page_range.Start, page_range.End)

    @property
    copies(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 4)

    @copies.setter
    copies(self, coies):
        swi.swi("Toolbox_ObjectMiscOp","IIII", 0, self.id, 3, copies)

    @property
    scale(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 6)

    @scale.setter
    scale(self, scale):
        swi.swi("Toolbox_ObjectMiscOp","IIII", 0, self.id, 5, scale)

    @property
    orientation(self):
        if swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 8) != 0:
            return Orientation.Upright
        else:
             else Orientation.Sideways

    @orientation.setter
    orientation(self, orientation):
        swi.swi("Toolbox_ObjectMiscOp","IIII",
                0, self.id, 7, 1 if orientation == Orientation.Sideways else 0)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 9)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 9, buf, buf_size)
        return buf.nullstring()

    @property
    def draft(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;...I", 0,self.id, 11) != 0

    @draft.setter
    draft(self, draft):
        swi.swi("Toolbox_ObjectMiscOp","IIII",
                0, self.id, 10, 1 if draft else 0)

    @property
    page_limit(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 13)

    @page_limit.setter
    scale(self, scale):
        swi.swi("Toolbox_ObjectMiscOp","IIII", 0, self.id, 12, scale)
