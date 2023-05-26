"""RISC OS Toolbox - ProgInfo"""

from ..base import Object
from enum import IntEnum
import swi

class ProgInfo(Object):
    class_id = 0x82b40

    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    LaunchWebPage     = class_id + 2

    LicenceType = IntEnum(
        "LicenceType",
        "PublicDomain SingleUser SingleMachine Site Network Authority".split(),
        start=0)

    @property
    def window_id(self):
        return swi.swi("Toolbox_ObjectMiscOp","0II;I", self.id, 0)

    @property
    def version(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 2)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 5, buf, buf_size)
        return buf.nullstring()

    @version.setter
    def version(self, version):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs', self.id, 1, version)

    @property
    def licence_type(self):
        return ProgInfo.LicenceType(
                   swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.id, 4))

    @licence_type.setter
    def license_type(self, licence_type):
        return swi.swi("Toolbox_ObjectMiscOp","0III", self.id, 3, licence_type)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 6)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 5, buf, buf_size)
        return buf.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 5, title)

    @property
    def uri(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 8)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 8, buf, buf_size)
        return buf.nullstring()

    @uri.setter
    def uri(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 7, title)

    @property
    def web_event(self):
        return swi.swi("Toolbox_ObjectMiscOp","0II;I", self.id, 10)

    @web_event.setter
    def web_event(self, web_event):
        swi.swi('Toolbox_ObjectMiscOp', '0III', self.id, 9, web_event)
