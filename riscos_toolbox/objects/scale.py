"""RISC OS Toolbox - Scale"""

import swi
import ctypes

from ..base import Object
from ..events import ToolboxEvent, AboutToBeShownEvent


class Scale(Object):
    class_id = 0x82c00

    AboutToBeShown = class_id + 0
    DialogueCompleted = class_id + 1
    ApplyFactor = class_id + 2

    @property
    def window_id(self):
        return self._miscop_get_unsigned(0)

    @property
    def value(self):
        return self._miscop_get_unsigned(2)

    @value.setter
    def value(self, value):
        self._miscop_set_sunsigned(1, value)

    @property
    def bounds(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'III;....iii', 0, self.id, 4)

    @bounds.setter
    def value(self, lower, upper, step):
        swi.swi('Toolbox_ObjectMiscOp', 'IIIiii', 0, self.id, 3,
                lower, upper, step)

    @property
    def title(self):
        return self._miscop_get_string(6)

    @title.setter
    def title(self, title):
        self._miscop_set_string(5, title)

# Scale events


class ScaleAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = Scale.AboutToBeShown


class ScaleDialogueCompletedEvent(ToolboxEvent):
    event_id = Scale.DialogueCompleted


class ScaleApplyFactorEvent(ToolboxEvent):
    event_id = Scale.ApplyFactor
    _fields_ = [("factor", ctypes.c_int32)]


# Deprecated versions
ApplyFactorEvent = ScaleApplyFactorEvent
