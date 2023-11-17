"""RISC OS Toolbox - Gadgets - Draggable"""

import ctypes
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
    DragStarted = 0x82887  # Window_SWIChunkBase (0x82880) + 7
    DragEnded   = 0x82888  # Window_SWIChunkBase (0x82880) + 8

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
        return self._miscop_get_string(Draggable.GetSprite)

    @sprite.setter
    def sprite(self, sprite):
        return self._miscop_set_string(Draggable.SetSprite, sprite)

    @property
    def text(self):
        return self._miscop_get_string(Draggable.GetText)

    @text.setter
    def text(self, text):
        return self._miscop_set_string(Draggable.SetText, text)

    @property
    def state(self):
        return self._miscop_get_signed(self.GetState) != 0

    @state.setter
    def state(self, state):
        return self._miscop_set_signed(Draggable.SetState, 1 if state else 0)


class DraggableDefinition(GadgetDefinition):
    _gadget_class = Draggable
    _fields_ = [
        ("text", ctypes.c_char_p),
        ("max_text_len", ctypes.c_int32),
        ("sprite", ctypes.c_char_p),
        ("max_sprite_len", ctypes.c_int32)
    ]


class DraggableDragStartedEvent(ToolboxEvent):
    event_id = Draggable.DragStarted


class _Wimp(ctypes.Structure):
    _fields_ = [
        ('window_handle', ctypes.c_int32),
        ('icon_handle', ctypes.c_int32),
    ]


class _Toolbox(ctypes.Structure):
    _fields_ = [
        ('window_id', ctypes.c_uint32),
        ('component_id', ctypes.c_uint32),
    ]


class _Target(ctypes.Union):
    _fields_ = [
        ('wimp', _Wimp),
        ('toolbox', _Toolbox),
    ]


class DraggableDragEndedEvent(ToolboxEvent):

    event_id = Draggable.DragEnded
    _anonyumous_ = ('_target',)
    _fields_ = [
        ('_target', _Target),
        ('_x', ctypes.c_int32),
        ('_y', ctypes.c_int32),
    ]

    @property
    def window_handle(self):
        return self.wimp.window_handle

    @property
    def icon_handle(self):
        return self.wimp.icon_handle

    @property
    def winddow_id(self):
        return self.toolbox.window_id

    @property
    def component_id(self):
        return self.toolbox.component_id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
