"""RISC OS Toolbox - ColourDBox"""

import swi

from ..base import Object
from enum import Enum

class ColourDbox(Object):
    class_id = 0x829c0
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    ColourSelected    = class_id + 2

    ColourModel = Enum("ColourModel", ["RGB", "CMYK", "HSV"])

    @property
    def colour(self):
        colour = swi.swi("Toolbox_ObjectMiscOp","III;i", 0,self.id, 1)
        return colour if colour > 0 else None

    @colour.setter
    def colour(self, colour):
        swi.swi("Toolbox_ObjectMiscOp","IIIi",
                0, self.id, 1, colour if colour else -1)

    @property
    def none_available(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;...I", 0,self.id, 3) != 0

    @none_available.setter
    def none_available(self, available):
        swi.swi("Toolbox_ObjectMiscOp","IIII",
                0, self.id, 2, 1 if available else 0)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 5)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 5, buf, buf_size)
        return buf.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 4, title)
