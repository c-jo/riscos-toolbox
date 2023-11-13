"""RISC OS Toolbox - DCS"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent


class DCS(Object):
    class_id = 0x82a80
    # Methods
    GetWindowId = 0
    SetMessage = 1
    GetMessage = 2
    SetTitle = 3
    GetTitle = 4
    # Events
    AboutToBeShown    = class_id + 0
    Discard           = class_id + 1
    Save              = class_id + 2
    DialogueCompleted = class_id + 3
    Cancel            = class_id + 4

    @property
    def window_id(self):
        return self._miscop_get_signed(DCS.GetWindowId)

    @property
    def message(self):
        return self._miscop_get_string(DCS.GetMessage)

    @message.setter
    def message(self, message):
        self._miscop_set_string(DCS.SetMessage, message)

    @property
    def title(self):
        return self._miscop_get_string(DCS.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(DCS.SetTitle, title)


# DCS events
class DCSAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = DCS.AboutToBeShown


class DCSDiscardEvent(ToolboxEvent):
    event_id = DCS.Discard


class DCSSaveEvent(ToolboxEvent):
    event_id = DCS.Save


class DCSDialogueCompletedEvent(ToolboxEvent):
    event_id = DCS.DialogueCompleted


class DCSCancelEvent(ToolboxEvent):
    event_id = DCS.Cancel
