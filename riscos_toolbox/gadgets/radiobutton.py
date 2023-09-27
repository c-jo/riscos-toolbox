# Module implementing Toolbox's RadioButton gadget.

import ctypes
import swi
from riscos_toolbox.gadgets import Gadget, GadgetDefinition
from riscos_toolbox.events import ToolboxEvent

class RadioButton(Gadget):
    _type = 384

    # Methods
    SetLabel = _type + 0
    GetLabel = _type + 1
    SetEvent = _type + 2
    GetEvent = _type + 3
    SetState = _type + 4
    GetState = _type + 5
    SetFont  = _type + 6

    # Events
    StateChanged = 0x82883 # Window SWI Chunk Base (0x82880) + 3

    # Flags
    GenerateUserStateChanged = 0x00000001
    GenerateSetStateChanged  = 0x00000002
    On                       = 0x00000004

    @property
    def label(self):
        return self._miscop_get_text(RadioButton.GetLabel)

    @label.setter
    def label(self, text):
        self._miscop_set_text(RadioButton.SetLabel,text)

    @property
    def event(self):
        return self._miscop_get_int(RadioButton.GetEvent)

    @event.setter
    def event(self, event):
        self._miscop_set_int(RadioButton.SetEvent,event)

    @property
    def state(self):
        return self._miscop_get_int(RadioButton.GetState)

    @state.setter
    def state(self, state):
        self._miscop_set_int(RadioButton.SetState,state)

    # Note: there is no GetFont method for this gadget.
    def set_font(self,font,width,height):
        swi.swi('Toolbox_ObjectMiscOp','0iiisII',self.window.id,RadioButton.SetFont,
                self.id,font,width,height)


class RadioButtonDefinition(GadgetDefinition):
    _gadget_class = RadioButton
    _fields_ = [ ("group_number", ctypes.c_int32),
                 ("label", ctypes.c_char_p),
                 ("max_label_len", ctypes.c_int32),
                 ("event", ctypes.c_int32) ]

class RadioButtonStateChangedEvent(ToolboxEvent):
    event_id = RadioButton.StateChanged

    _fields_ = [ ("_state", ctypes.c_int32),
                 ("_old_on_button", ctypes.c_int32) ]

    # Event constants
    Adjust = 0x00000001
    Select = 0x00000004

    @property
    def state(self):
        return self._state

    @property
    def old_on_button(self):
        return self._old_on_button

