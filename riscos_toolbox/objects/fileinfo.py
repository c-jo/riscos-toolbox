"""RISC OS Toolbox - FileInfo"""

from ..base import Object
from ..events import ToolboxEvent, AboutToBeShownEvent
import datetime
import swi

_ro_epoch = datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)


class FileInfo(Object):
    class_id = 0x82ac0
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1

    @property
    def window_id(self):
        return self._miscop_get_unsigned(0)

    @property
    def modified(self):
        return self._miscop_get_unsigned(2) != 0

    @modified.setter
    def modified(self, modified):
        self._miscop_set_unsigned(1, 1 if modified else 0)

    @property
    def file_type(self):
        return self._miscop_get_signed(4)

    @file_type.setter
    def file_type(self, file_type):
        self._miscop_set_signed(3)

    @property
    def file_name(self):
        return self._miscop_get_string(6)

    @file_name.setter
    def file_name(self, file_name):
        self._miscop_set_string(5, file_name)

    @property
    def file_size(self):
        return self._miscop_get_signed(8)

    @file_size.setter
    def file_size(self, file_size):
        self._miscop_set_signed(7, file_size)

    @property
    def date(self):
        timebuf = swi.block(2)
        swi.swi('Toolbox_ObjectMiscOp', '0IIb', self.id, 10, timebuf)
        quin = timebuf[0] + timebuf[1] << 32
        return _ro_epoch + datetime.timedelta(seconds=quin / 100).astimezone()

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
        return self._miscop_get_string(11)

    @title.setter
    def title(self, title):
        self._miscop_set_string(10, title)


# FileInfo Events
class AboutToBeShownEvent(AboutToBeShownEvent):
    event_id = FileInfo.AboutToBeShown


class DialogueCompletedEvent(ToolboxEvent):
    event_id = FileInfo.DialogueCompleted
