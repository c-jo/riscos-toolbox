"""RISC OS Toolbox - FileInfo"""

from ..base import Object
from ..events import ToolboxEvent, AboutToBeShownEvent
import datetime
import swi

_ro_epoch = datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)


class FileInfo(Object):
    class_id = 0x82ac0
    # Methods
    GetWindowId = 0
    SetModified = 1
    GetModified = 2
    SetFileType = 3
    GetFileType = 4
    SetFileName = 5
    GetFileName = 6
    SetFileSize = 7
    GetFileSize = 8
    SetDate     = 9
    GetDate     = 10
    SetTitle    = 11
    GetTitle    = 12
    # Events
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1

    @property
    def window_id(self):
        return self._miscop_get_unsigned(FileInfo.GetWindowId)

    @property
    def modified(self):
        return self._miscop_get_unsigned(FileInfo.GetModified) != 0

    @modified.setter
    def modified(self, modified):
        self._miscop_set_unsigned(FileInfo.SetModified, 1 if modified else 0)

    @property
    def file_type(self):
        return self._miscop_get_signed(FileInfo.GetFileType)

    @file_type.setter
    def file_type(self, file_type):
        self._miscop_set_signed(FileInfo.SetFileType, file_type)

    @property
    def file_name(self):
        return self._miscop_get_string(FileInfo.GetFileName)

    @file_name.setter
    def file_name(self, file_name):
        self._miscop_set_string(FileInfo.SetFileName, file_name)

    @property
    def file_size(self):
        return self._miscop_get_signed(FileInfo.GetFileSize)

    @file_size.setter
    def file_size(self, file_size):
        self._miscop_set_signed(FileInfo.SetFileSize, file_size)

    @property
    def date(self):
        timebuf = swi.block(2)
        swi.swi('Toolbox_ObjectMiscOp', 'IiIb',
                0, self.id, FileInfo.GetDate, timebuf)
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
        swi.swi('Toolbox_ObjectMiscOp', 'IiIb',
                0, self.id, FileInfo.SetDate, timebuf)

    @property
    def title(self):
        return self._miscop_get_string(FileInfo.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(FileInfo.SetTitle, title)


# FileInfo Events
class AboutToBeShownEvent(AboutToBeShownEvent):
    event_id = FileInfo.AboutToBeShown


class DialogueCompletedEvent(ToolboxEvent):
    event_id = FileInfo.DialogueCompleted
