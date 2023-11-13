"""RISC OS Toolbox - Gadgets - ActionButton"""

from . import Gadget
from ..events import ToolboxEvent


class ActionButton(Gadget):
    _type = 128
    SetText      = _type + 0
    GetText      = _type + 1
    SetEvent     = _type + 2
    GetEvent     = _type + 3
    SetClickShow = _type + 4
    GetClickShow = _type + 5
    SetFont      = _type + 6

    # Events
    Selected = 0x82881  # Window_SWIChunkBase (0x82880) + 1

    # Flags
    IsDefault          = 0x00000001
    IsCancel           = 0x00000002
    IsLocal            = 0x00000004
    ClickShowTransient = 0x00000008
    ClickShowCentred   = 0x00000010
    ClickShowAtPointer = 0x00000020

    # Properties
    @property
    def text(self):
        return self._miscop_get_string(ActionButton.GetText)

    @text.setter
    def text(self, text):
        self._miscop_set_string(ActionButton.SetText, text)

    @property
    def event(self):
        return self._miscop_get_unsigned(ActionButton.GetEvent)

    @event.setter
    def event(self, ev):
        return self._miscop_set_signed(ActionButton.SetEvent, ev)

    @property
    def click_show(self):
        return self._miscop_get_unsigned(ActionButton.GetClickShow)

    @click_show.setter
    def click_show(self, click_show):
        self._miscop_set_unsigned(ActionButton.SetClickShow, click_show)

    # Methods
    def set_font(self, *args, **kwargs):
        self._miscop_set_font(ActionButton.SetFont, *args, **kwargs)


class ActionButtonSelectedEvent(ToolboxEvent):
    event_id = ActionButton.Selected
    # Flags
    Adjust  = 0x00000001
    Select  = 0x00000004
    Default = 0x00000008
    Cancel  = 0x00000010
    Local   = 0x00000020

    # Properties
    @property
    def adjust(self):
        return self.flags & ActionButtonSelectedEvent.Adjust

    @property
    def select(self):
        return self.flags & ActionButtonSelectedEvent.Select

    @property
    def default(self):
        return self.flags & ActionButtonSelectedEvent.Defaut

    @property
    def cancel(self):
        return self.flags & ActionButtonSelectedEvent.Cancel

    @property
    def local(self):
        return self.flags & ActionButtonSelectedEvent.Local


# For anything using the old name.
SelectedEvent = ActionButtonSelectedEvent
