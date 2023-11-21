"""RISC OS Toolbox - PrintDbox"""

import ctypes
import swi
from enum import Enum
from collections import namedtuple

from ..base import Object
from ..events import ToolboxEvent, AboutToBeShownEvent

Orientation = Enum("Orientation", ["Sideways", "Upright"])
PageRange = namedtuple("PageRange", ["Start", "End"])


class PrintDbox(Object):
    class_id = 0x82b00
    # Methods
    GetWindowId    = 0
    SetPageRange   = 1
    GetPageRange   = 2
    SetCopies      = 3
    GetCopies      = 4
    SetScale       = 5
    GetScale       = 6
    SetOrientation = 7
    GetOrientation = 8
    GetTitle       = 9
    SetDraft       = 10
    GetDraft       = 11
    # Events
    AboutToBeShown      = class_id + 0
    DialogueCompleted   = class_id + 1
    SetupAboutToBeShown = class_id + 2
    Save                = class_id + 3
    Setup               = class_id + 4
    Print               = class_id + 5
    # Constants
    PrintSave_Sideways = 0x00000001
    PrintSave_Draft    = 0x00000002

    @property
    def window_id(self):
        return self._miscop_get_unsigned(PrintDbox.GetWindowId)

    @property
    def page_range(self):
        return PageRange(swi.swi(
            'Toolbox_ObjectMiscOp', 'III;ii', 0, self.id, PrintDbox.GetPageRange))

    @page_range.setter
    def page_range(self, page_range):
        swi.swi('Toolbox_ObjectMiscOp', 'IIIii',
                0, self.id, PrintDbox.SetPageRange, page_range.Start, page_range.End)

    @property
    def copies(self):
        return self._miscop_get_signed(PrintDbox.GetCopies)

    @copies.setter
    def copies(self, copies):
        self._miscop_set_signed(PrintDbox.SetCopies, copies)

    @property
    def scale(self):
        return self._miscop_get_signed(PrintDbox.GetScale)

    @scale.setter
    def scale(self, scale):
        self._miscop_set_signed(PrintDbox.SetScale, scale)

    @property
    def orientation(self):
        orientation = self._miscop_get_unsigned(PrintDbox.GetOrientation)
        return Orientation.Upright if orientation == 0 else Orientation.Sideways

    @orientation.setter
    def orientation(self, orientation):
        self._miscop_set_unsigned(
            PrintDbox.SetOrientation, 0 if orientation == Orientation.Upright else 1)

    @property
    def title(self):
        self._miscop_get_string(PrintDbox.GetTitle)

    @property
    def draft(self):
        return self._miscop_get_unsigned(PrintDbox.GetDraft) != 0

    @draft.setter
    def draft(self, draft):
        self._miscop_set_unsigned(PrintDbox.SetDraft, 1 if draft else 0)


class PrintDboxAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = PrintDbox.AboutToBeShown


class PrintDboxDialogueCompletedEvent(ToolboxEvent):
    event_id = PrintDbox.DialogueCompleted


class PrintDboxSetupAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = PrintDbox.SetupAboutToBeShown


class PrintDboxSaveEvent(ToolboxEvent):
    event_id = PrintDbox.Save
    _field_ = [
        ("start_page", ctypes.c_int32),
        ("finish_page", ctypes.c_int32),
        ("copies", ctypes.c_int32),
        ("scale_factor", ctypes.c_int32),
    ]

    @property
    def sideways(self):
        return self.flags & PrintDbox.PrintSave_Sideways != 0

    @property
    def draft(self):
        return self.flags & PrintDbox.PrintSave_Draft != 0


class PrintDboxSetUpEvent(ToolboxEvent):
    event_id = PrintDbox.Setup


class PrintDboxPrintEvent(ToolboxEvent):
    event_id = PrintDbox.Print

    _fields_ = [
        ("start_page", ctypes.c_int32),
        ("finish_page", ctypes.c_int32),
        ("copies", ctypes.c_int32),
        ("scale_factor", ctypes.c_int32),
    ]

    @property
    def sideways(self):
        return self.flags & PrintDbox.PrintSave_Sideways != 0

    @property
    def draft(self):
        return self.flags & PrintDbox.PrintSave_Draft != 0


# For compatability with 1.0.2 and below
PrintEvent = PrintDboxPrintEvent
