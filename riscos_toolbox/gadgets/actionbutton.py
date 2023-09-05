"""RISC OS Toolbox - Gadgets - ActionButton"""

from . import Gadget
from ..events import ToolboxEvent

import swi

class ActionButton(Gadget):

    # Events
    Selected = 0x82881
    # Flags
    IsDefault          = 0x00000001
    IsCancel           = 0x00000002
    IsLocal            = 0x00000004
    ClickShowTransient = 0x00000008
    ClickShowCentred   = 0x00000010
    ClickShowAtPointer = 0x00000020

    @property
    def text(self):
        return self._miscop_get_text(129)

    @text.setter
    def text(self, text):
        self._miscop_set_text(128, text)

    @property
    def event(self):
        return self._miscop_get_int(131)

    @event.setter
    def event(self, ev):
        return self._miscop_set_int(130, ev)

    @property
    def click_show(self):
        return self._miscop_get_int(133)

    @click_show.setter
    def click_show(self, cs):
        return self._miscop_get_int(132, cs)

class ActionButtonSelectedEvent(ToolboxEvent):
    event_id = ActionButton.Selected
    # Flags
    Adjust  = 0x00000001
    Select  = 0x00000004
    Default = 0x00000008
    Cancel  = 0x00000010
    Local   = 0x00000020

# For anything using the old name.
SelectedEvent = ActionButtonSelectedEvent
