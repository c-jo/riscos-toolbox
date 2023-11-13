# Module implementing the Toolbox's Adjsuter gadget.

import ctypes
from riscos_toolbox.gadgets import Gadget
from riscos_toolbox.events import ToolboxEvent


class Adjuster(Gadget):
    _type = 768

    # Events
    AdjusterClicked = 0x8288C  # Window_SWIChunkBase (0x82880) + 12

    # Flags
    Increment = 0x00000001
    Decrement = 0x00000000
    UpDown    = 0x00000002
    LeftRight = 0x00000000


class AdjusterClickedEvent(ToolboxEvent):
    event_id = Adjuster.AdjusterClicked

    _fields_ = [("_direction", ctypes.c_int32)]

    @property
    def direction(self):
        return self._direction

    @property
    def down(self):
        return self._direction == 0

    @property
    def up(self):
        return self._direction == 1
