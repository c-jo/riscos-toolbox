# Module implementing the Toolbox's NumberRange gadget.

import ctypes
import swi
from riscos_toolbox.gadgets import Gadget, GadgetDefinition
from riscos_toolbox.events import ToolboxEvent


class NumberRange(Gadget):
    _type = 832

    # Methods
    SetValue      = _type + 0
    GetValue      = _type + 1
    SetBounds     = _type + 2
    GetBounds     = _type + 3
    GetComponents = _type + 4

    # Events
    ValueChanged = 0x8288D  # Window_SWIChunkBase (0x82880) + 13

    # Gadget Flags
    GenerateUserValueChanged = 0x00000001
    GenerateSetValueChanged  = 0x00000002
    Writable                 = 0x00000004
    HasNumericalDisplay      = 0x00000008
    Adjusters                = 0x00000010
    NoSlider                 = 0x00000000
    SliderType               = 0x00000020
    SliderRight              = 0x00000020
    SliderLeft               = SliderRight * 2
    SliderColour             = 0x00000100
    SliderTypeMask           = 0x000000E0

    # Method Flags
    NumericalField = 0x00000001
    LeftAdjuster   = 0x00000002
    RightAdjuster  = 0x00000004
    Slider         = 0x00000008
    LowerBound     = 0x00000001
    UpperBound     = 0x00000002
    StepSize       = 0x00000004
    Precision      = 0x00000008

    # Getters and setters
    @property
    def value(self):
        return self._miscop_get_signed(NumberRange.GetValue)

    @value.setter
    def value(self, value):
        self._miscop_set_signed(NumberRange.SetValue, value)

    # Bounds
    @property
    def bounds(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;ii',
            NumberRange.LowerBound | NumberRange.UpperBound,
            self.window.id,
            NumberRange.GetBounds,
            self.id)

    @property
    def lower_bound(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;i...',
            NumberRange.LowerBound,
            self.window.id,
            NumberRange.GetBounds,
            self.id)

    @lower_bound.setter
    def lower_bound(self, lower):
        # Protect against setting both bounds to the same value
        if lower == self.upper_bound:
            lower -= 1
        swi.swi(
            'Toolbox_ObjectMiscOp', 'IIIIi000',
            NumberRange.LowerBound,
            self.window.id,
            NumberRange.SetBounds,
            self.id,
            lower)

    @property
    def upper_bound(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;.i..',
            NumberRange.UpperBound,
            self.window.id,
            NumberRange.GetBounds,
            self.id)

    @upper_bound.setter
    def upper_bound(self, upper):
        # Protect against setting both bounds to the same value
        if upper == self.lower_bound:
            upper += 1
        swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII0i00',
            NumberRange.UpperBound,
            self.window.id,
            NumberRange.SetBounds,
            self.id,
            upper)

    @property
    def step_size(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;..i.',
            NumberRange.StepSize,
            self.window.id,
            NumberRange.GetBounds,
            self.id)

    @step_size.setter
    def step_size(self, step):
        swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII00i0',
            NumberRange.StepSize,
            self.window.id,
            NumberRange.SetBounds,
            self.id,
            step)

    @property
    def precision(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;...i',
            NumberRange.Precision,
            self.window.id,
            NumberRange.GetBounds,
            self.id)

    @precision.setter
    def precision(self, precision):
        swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII000i',
            NumberRange.Precision,
            self.window.id,
            NumberRange.SetBounds,
            self.id,
            precision)

    # Components
    @property
    def numerical_field(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;i...',
            NumberRange.NumericalField,
            self.window.id,
            NumberRange.GetComponents,
            self.id)

    @property
    def left_adjuster(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;.i..',
            NumberRange.LeftAdjuster,
            self.window.id,
            NumberRange.GetComponents,
            self.id)

    @property
    def right_adjuster(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;..i.',
            NumberRange.RightAdjuster,
            self.window.id,
            NumberRange.GetComponents,
            self.id)

    @property
    def slider(self):
        return swi.swi(
            'Toolbox_ObjectMiscOp', 'IIII;...i',
            NumberRange.Slider,
            self.window.id,
            NumberRange.GetComponents,
            self.id)


class NumberRangeDefinition(GadgetDefinition):
    _gadget_class = NumberRange
    _fields_ = [
        ("lower_bound", ctypes.c_int32),
        ("upper_bound", ctypes.c_int32),
        ("step_size", ctypes.c_int32),
        ("initial_value", ctypes.c_int32),
        ("precision", ctypes.c_int32),
        ("before", ctypes.c_int32),
        ("after", ctypes.c_int32),
        ("display_length", ctypes.c_int32),
    ]


class NumberRangeValueChangedEvent(ToolboxEvent):
    event_id = NumberRange.ValueChanged

    _fields_ = [("_new_value", ctypes.c_int32)]

    @property
    def new_value(self):
        return self._new_value
