"""RISC OS Toolbox - FileInfo"""

from ..base import Object
from ..events import ToolboxEvent, AboutToBeShownEvent
import datetime
import swi

_ro_epoch = datetime.datetime(1900,1,1,0,0,0,0,datetime.timezone.utc)

class FileInfo(Object):
    class_id = 0x82ac0
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1

    @property
    def window_id(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 0)

    @property
    def modified(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 2) != 0

    @modified.setter
    def modified(self, modified):
        swi.swi("Toolbox_ObjectMiscOp","IIII", 0, self.id, 1,
                1 if modified else 0)

    @property
    def file_type(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 4)

    @file_type.setter
    def file_type(self, file_type):
        swi.swi("Toolbox_ObjectMiscOp","IIII", 0, self.id, 3, file_type)

    @property
    def file_name(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 6)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 6, buf, buf_size)
        return buf.nullstring()

    @file_name.setter
    def file_name(self, file_name):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 5, file_name)

    @property
    def file_size(self):
        return swi.swi("Toolbox_ObjectMiscOp","III;I", 0, self.id, 8)

    @file_type.setter
    def file_size(self, file_size):
        swi.swi("Toolbox_ObjectMiscOp","IIII", 0, self.id, 7, file_size)

    @property
    def date(self):
        timebuf = swi.block(2)
        swi.swi('Toolbox_ObjectMiscOp', '0IIb', self.id, 10, timebuf)
        quin = timebuf[0] + timebuf[1] << 32
        return _ro_epoch + datetime.timedelta(seconds=quin/100).astimezone()

    @date.setter
    def date(self, date):
        if date.tzinfo is None:
            date = date.astimezone()
        quin = int((date - _ro_epoch).total_seconds() * 100)
        timebuf = swi.block(2)
        timebuf[0] = quin  % 0x100000000
        timebuf[1] = quin // 0x100000000
        swi.swi('Toolbox_ObjectMiscOp', '0IIb', self.id, 9, timebuf)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 11)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 11, buf, buf_size)
        return buf.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 10, title)


def AboutToBeShownEvent(AboutToBeShownEvent):
    event_id = FileInfo.AboutToBeShown

def DialogueCompletedEvent(ToolboxEvent):
    event_id = FileInfo.DialogueCompleted
