"""RISC OS Toolbox - Gadgets - Draggable"""

import ctypes
import swi
from . import Gadget, GadgetDefinition
from ..events import ToolboxEvent

class Draggable(Gadget):
    _type = 640

    # Methods
    SetSprite = _type + 0
    GetSprite = _type + 1
    SetText   = _type + 2
    GetText   = _type + 3
    SetState  = _type + 4
    GetState  = _type + 5

    # Events
    DragStarted = 0x82887 # Window_SWIChunkBase (0x82880) + 7
    DragEnded   = 0x82888 # Window_SWIChunkBase (0x82880) + 8

    # Flags
    GenerateDragStarted = 0x00000001
    Sprite              = 0x00000002
    TypeShift           = 0x00000003
    Text                = 0x00000004
    TypeMask            = 0x00000038
    ToolboxIds          = 0x00000040
    HasDropShadow       = 0x00000080
    NotDithered         = 0x00000100

    @property
    def sprite(self):
        return self._miscop_get_text(Draggable.GetSprite)

    @sprite.setter
    def sprite(self, sprite):
        return self._miscop_set_text(Draggable.SetSprite, sprite)

    @property
    def text(self):
        return self._miscop_get_text(Draggable.GetText)

    @text.setter
    def text(self, text):
        return self._miscop_set_text(Draggable.SetText, text)

    @property
    def state(self):
        return self._miscop_get_int(self.GetState)

    @state.setter
    def state(self, state):
        return self._miscop_set_int(Draggable.SetState, state)

class DraggableDefinition(GadgetDefinition):
    _gadget_class = Draggable
    _fields_ = [ ("text", ctypes.c_char_p),
                 ("max_text_len", ctypes.c_int32),
                 ("sprite", ctypes.c_char_p),
                 ("max_sprite_len", ctypes.c_int32) ]

class DraggableDragStartedEvent(ToolboxEvent):
    event_id = Draggable.DragStarted

    # This event actually doesn't have any fields other than the header
    _fields_ = [ ]

class DraggableDragEndedEvent(ToolboxEvent):
    event_id = Draggable.DragEnded

     # Note that window handle and icon handle here can be object/component ID if
     # ToolboxIds flag is set
    _fields_ = [ ("window_handle", ctypes.c_int32),
                 ("icon_handle", ctypes.c_int32),
                 ("x", ctypes.c_int32),
                 ("y", ctypes.c_int32) ]

    @property
    def window_handle(self):
        return self._window_handle

    @property
    def icon_handle(self):
        return self._icon_handle

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
