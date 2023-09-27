# Module implementing the Toolbox's Slider gadget.

import swi
import ctypes
from riscos_toolbox.gadgets import Gadget, GadgetDefinition
from riscos_toolbox.events import ToolboxEvent

class Slider(Gadget):
    _type = 576

    ## Methods
    SetValue  = _type + 0
    GetValue  = _type + 1
    SetBounds = _type + 2
    GetBounds = _type + 3
    SetColour = _type + 4
    GetColour = _type + 5

    # Events
    ValueChanged = 0x82886 # Window SWI Chunk Base (0x82880) + 6

    # Flags
    GenerateValueChangedEndOfDrag  = 0x00000001
    GenerateValueChangedDuringDrag = 0x00000002
    GenerateSetValueChanged        = 0x00000004
    Vertical                       = 0x00000008
    Draggable                      = 0x00000010
    BarColour                      = 0x0000F000
    BarColourShift                 = 12
    BackgroundColour               = 0x000F0000
    BackgroundColourShift          = 16

    # Method constants
    LowerBound = 0x00000001
    UpperBound = 0x00000002
    StepSize   = 0x00000004

    @property
    def value(self):
        return self._miscop_get_int(Slider.GetValue)

    @value.setter
    def value(self, value):
        self._miscop_set_int(Slider.SetValue, value)

    # Bounds have been split into separate properties - this seemed the most logical way
    @property
    def lower_bound(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;i',
                       Slider.LowerBound,self.window.id,Slider.GetBounds,self.id)

    @lower_bound.setter
    def lower_bound(self, lower):
        swi.swi('Toolbox_ObjectMiscOp','Iiiii',Slider.LowerBound,
                self.window.id,Slider.SetBounds,self.id,lower)

    @property
    def upper_bound(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;.i',
                       Slider.UpperBound,self.window.id,Slider.GetBounds,self.id)

    @upper_bound.setter
    def upper_bound(self, upper):
        swi.swi('Toolbox_ObjectMiscOp','Iiii.i',Slider.UpperBound,
                self.window.id,Slider.SetBounds,self.id,upper)

    @property
    def step_size(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;..i',
                       Slider.StepSize,self.window.id,Slider.GetBounds,self.id)

    @step_size.setter
    def step_size(self, step):
        swi.swi('Toolbox_ObjectMiscOp','Iiii..i',Slider.StepSize,
                self.window.id,Slider.SetBounds,self.id,step)

    # returns a tuple (fg, bg)
    @property
    def colour(self):
        return swi.swi('Toolbox_ObjectMiscOp','0iii;ii',self.window.id,Slider.GetColour,
                       self.id)

    # takes a tuple (fg, bg)
    @colour.setter
    def colour(self, colours):
        fg, bg = colours
        swi.swi('Toolbox_ObjectMiscOp','0iiiii',self.window.id,Slider.SetColour,
                self.id,fg,bg)

class SliderDefinition(GadgetDefinition):
    _gadget_class = Slider
    _fields_ = [ ("lower_bound", ctypes.c_int32),
                 ("upper_bound", ctypes.c_int32),
                 ("step_size", ctypes.c_int32),
                 ("initial_value", ctypes.c_int32) ]

class SliderValueChangedEvent(ToolboxEvent):
    event_id = Slider.ValueChanged

    _fields_ = [ ("_new_value", ctypes.c_int32) ]

    # Event Constants
    EndOfDrag  = 1
    DuringDrag = 2

    @property
    def new_value(self):
        return self._new_value

