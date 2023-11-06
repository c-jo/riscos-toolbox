"""RISC OS Toolbox - PrintDbox"""

import ctypes
import swi
from enum import Enum
from collections import namedtuple

from ..base import Object
from ..events import ToolboxEvent


class PrintDbox(Object):
    class_id = 0x82b00

    AboutToBeShown      = class_id + 0
    DialogueCompleted   = class_id + 1
    SetupAboutToBeShown = class_id + 2
    Save                = class_id + 3
    Setup               = class_id + 4
    Print               = class_id + 5

    Orientation = Enum("Orientation", ["Sideways", "Upright"])
    PageRange   = namedtuple("PageRange", ["Start", "End"])

    @property
    def window_id(self):
        return self._miscop_get_unsigned(0)

    @property
    def page_range(self):
        return PrintDbox.PageRange(swi.swi(
            'Toolbox_ObjectMiscOp', 'III;ii', 0, self.id, 2))

    @page_range.setter
    def page_range(self, page_range):
        swi.swi('Toolbox_ObjectMiscOp', 'IIIii',
                0, self.id, 1, page_range.Start, page_range.End)

    @property
    def copies(self):
        return self._miscop_get_signed(4)

    @copies.setter
    def copies(self, copies):
        self._miscop_set_copied(3, copies)

    @property
    def scale(self):
        return self._miscop_get_signed(6)

    @scale.setter
    def scale(self, scale):
        self._miscop_set_copied(5, scale)

    @property
    def orientation(self):
        if self._miscop_get_unsigned(8) == 0:
            return PrintDbox.Orientation.Upright
        else:
            return PrintDbox.Orientation.Sideways

    @orientation.setter
    def orientation(self, orientation):
        self._miscop_set_unsigned(
            7, 0 if orientation == PrintDbox.Orientation.Upright else 1)

    @property
    def title(self):
        self._miscop_get_string(9)

    @property
    def draft(self):
        return self._miscop_get_unsigned(11) != 0

    @draft.setter
    def draft(self, draft):
        self._miscop_set_unsigned(10, 1 if draft else 0)

    @property
    def page_limit(self):
        return self._miscop_get_unsigned(13)

    @page_limit.setter
    def page_limit(self, limit):
        self._miscop_set_unsigned(12, limit)


class PrintEvent(ToolboxEvent):
    event_id = PrintDbox.Print

    _fields_ = [
        ("start_page", ctypes.c_int32),
        ("finish_page", ctypes.c_int32),
        ("copies", ctypes.c_int32),
        ("scale_factor", ctypes.c_int32),
    ]

    @property
    def sideways(self):
        return self.flags & 0x01 != 0

    @property
    def draft(self):
        return self.flags & 0x02 != 0
