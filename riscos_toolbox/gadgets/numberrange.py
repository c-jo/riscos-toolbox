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
    ValueChanged = 0x8288D # Window_SWIChunkBase (0x82880) + 13

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
        return self._miscop_get_int(NumberRange.GetValue)

    @value.setter
    def value(self, value):
        self._miscop_set_int(NumberRange.SetValue, value)


    # For bounds and components, it's made the most sense to me to split these into separate
    # properties rather than having bespoke methods to return tuples or something.

    # Bounds
    @property
    def lower_bound(self):
        # ObjectId and ComponentId are signed ints
        # The parent class's _miscop_get_int always passes 0 to flags, so we need
        # to do our own here
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;i',NumberRange.LowerBound,
                        self.window.id,NumberRange.GetBounds,self.id)

    @lower_bound.setter
    def lower_bound(self, value):
        swi.swi('Toolbox_ObjectMiscOp','Iiiii',NumberRange.LowerBound,self.window.id,
                NumberRange.SetBounds,self.id,value)

    @property
    def upper_bound(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;.i',NumberRange.UpperBound,
                       self.window.id,NumberRange.GetBounds,self.id)
    # If upper bound is set to lower bound, a divide by zero occurs, so
    # this setter will check for that and set it to one more than lower if this is the case.
    @upper_bound.setter
    def upper_bound(self, value):
        if value == self.lower_bound:
            value += 1
        swi.swi('Toolbox_ObjectMiscOp','Iiii.i',NumberRange.UpperBound,self.window.id,
                NumberRange.SetBounds,self.id,value)

    @property
    def step_size(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;..i',NumberRange.StepSize,
                       self.window.id,NumberRange.GetBounds,self.id)

    @step_size.setter
    def step_size(self, value):
        swi.swi('Toolbox_ObjectMiscOp','Iiii..i',NumberRange.StepSize,self.window.id,
                NumberRange.SetBounds,self.id,value)

    @property
    def precision(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;...i',NumberRange.Precision,
                       self.window.id,NumberRange.GetBounds,self.id)

    @precision.setter
    def precision(self, value):
        swi.swi('Toolbox_ObjectMiscOp','Iiii...i',NumberRange.Precision,self.window.id,
                NumberRange.SetBounds,self.id,value)

    # Components

    @property
    def numeric(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;i',NumberRange.NumericalField,
                       self.window.id,NumberRange.GetComponents,self.id)

    @property
    def left_adjuster(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;.i',NumberRange.LeftAdjuster,
                       self.window.id,NumberRange.GetComponents,self.id)

    @property
    def right_adjuster(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;..i',NumberRange.RightAdjuster,
                       self.window.id,NumberRange.GetComponents,self.id)

    @property
    def slider(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;...i',NumberRange.Slider,
                       self.window.id,NumberRange.GetComponents,self.id)


class NumberRangeDefinition(GadgetDefinition):
    _gadget_class = NumberRange
    _fields_ = [ ("lower_bound", ctypes.c_int32),
                ("upper_bound", ctypes.c_int32),
                ("step_size", ctypes.c_int32),
                ("initial_value", ctypes.c_int32),
                ("precision", ctypes.c_int32),
                ("before", ctypes.c_int32),
                ("after", ctypes.c_int32),
                ("display_length", ctypes.c_int32) ]

class NumberRangeValueChangedEvent(ToolboxEvent):
    event_id = NumberRange.ValueChanged

    _fields_ = [ ("_new_value", ctypes.c_int32) ]

    @property
    def new_value(self):
        return self._new_value
