"""RISC OS Toolbox - Scale"""

import swi
import ctypes

from ..base import Object
from ..events import ToolboxEvent, AboutToBeShownEvent


class Scale(Object):
    class_id = 0x82c00
    # Methods
    GetWindowId = 0
    SetValue    = 1
    GetValue    = 2
    SetBounds   = 3
    GetBounds   = 4
    SetTitle    = 5
    GetTitle    = 6
    # Events
    AboutToBeShown = class_id + 0
    DialogueCompleted = class_id + 1
    ApplyFactor = class_id + 2
    # Constants
    SetLowerBound = 0x00000001
    SetUpperBound = 0x00000002
    SetStepSize   = 0x00000004

    @property
    def window_id(self):
        return self._miscop_get_unsigned(Scale.GetWindowId)

    @property
    def value(self):
        return self._miscop_get_unsigned(Scale.GetValue)

    @value.setter
    def value(self, value):
        self._miscop_set_sunsigned(Scale.SetValue, value)

    @property
    def lower_bound(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'III;i..',
                       0, self.id, Scale.GetBounds)

    @lower_bound.setter
    def lower_bound(self, lower_bound):
        swi.swi('Toolbox_ObjectMiscOp', 'IIIi00',
                Scale.SetLowerBound, self.id, Scale.SetBounds, lower_bound)

    @property
    def upper_bound(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'III;.i.',
                       0, self.id, Scale.GetBounds)

    @upper_bound.setter
    def upper_bound(self, upper_bound):
        swi.swi('Toolbox_ObjectMiscOp', 'III0i0',
                Scale.SetUpperBound, self.id, Scale.SetBounds, upper_bound)

    @property
    def step_size(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'III;..i',
                       0, self.id, Scale.GetBounds)

    @step_size.setter
    def step_size(self, step_size):
        swi.swi('Toolbox_ObjectMiscOp', 'III00i',
                Scale.SetStepSize, self.id, Scale.SetBounds, step_size)

    @property
    def title(self):
        return self._miscop_get_string(Scale.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(Scale.SetTitle, title)


class ScaleAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = Scale.AboutToBeShown


class ScaleDialogueCompletedEvent(ToolboxEvent):
    event_id = Scale.DialogueCompleted


class ScaleApplyFactorEvent(ToolboxEvent):
    event_id = Scale.ApplyFactor
    _fields_ = [("factor", ctypes.c_int32)]


# For compatability with 1.0.2 and below
ApplyFactorEvent = ScaleApplyFactorEvent
