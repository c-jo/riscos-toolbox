# Classes for the OptionButton gadget

import ctypes
import swi
from riscos_toolbox.gadgets import Gadget, GadgetDefinition
from riscos_toolbox.events import ToolboxEvent

class OptionButton(Gadget):
    _type = 192

    # Methods
    SetLabel = _type + 0
    GetLabel = _type + 1
    SetEvent = _type + 2
    GetEvent = _type + 3
    SetState = _type + 4
    GetState = _type + 5

    # Events
    StateChanged = 0x82882 # Window_SWIChunkBase (0x82880) + 2

    # Flags
    StateChanged_Adjust = 0x00000001
    StateChanged_Select = 0x00000004

    # Getters and setters go here
    @property
    def label(self):
        return self._miscop_get_text(OptionButton.GetLabel)

    @label.setter
    def label(self, label):
        return self._miscop_set_text(OptionButton.SetLabel, label)

    @property
    def event(self):
        return self._miscop_get_int(OptionButton.GetEvent)

    @event.setter
    def event(self, event):
        return self._miscop_set_int(OptionButton.SetEvent, event)

    @property
    def state(self):
        return self._miscop_get_int(OptionButton.GetState)

    @state.setter
    def state(self, state):
        return self._miscop_set_int(OptionButton.SetState, state)

class OptionButtonDefinition(GadgetDefinition):
    _gadget_class = OptionButton
    _fields_ = [ ("label", ctypes.c_char_p),
                ("max_label_len", ctypes.c_int32),
                ("event", ctypes.c_int32) ]

class OptionButtonStateChangedEvent(ToolboxEvent):
    event_id = OptionButton.StateChanged

    _fields_ = [ ("new_state", ctypes.c_int32) ]

    @property
    def new_state(self):
        return self._new_state
