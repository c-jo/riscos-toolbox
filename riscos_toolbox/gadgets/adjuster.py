# Module implementing the Toolbox's Adjsuter gadget.

import ctypes
from riscos_toolbox.gadgets import Gadget
from riscos_toolbox.events import ToolboxEvent

class Adjuster(Gadget):
    _type = 768

    # This gadget has no methods or useful fields.
    # However, it does have one event and a few flags.
    AdjusterClicked = 0x8288C # Window SWI chunk base (0x82880) + 12

    # Flags
    Increment = 0x00000001
    Decrement = 0x00000000
    UpDown    = 0x00000002
    LeftRight = 0x00000000

class AdjusterClickedEvent(ToolboxEvent):
    event_id = Adjuster.AdjusterClicked

    _fields_ = [ ("_direction", ctypes.c_int32) ]

    @property
    def direction(self):
        return self._direction
