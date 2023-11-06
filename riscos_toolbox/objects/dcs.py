"""RISC OS Toolbox - DCS"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent


class DCS(Object):
    class_id = 0x82a80
    AboutToBeShown    = class_id + 0
    Discard           = class_id + 1
    Save              = class_id + 2
    DialogueCompleted = class_id + 3
    Cancel            = class_id + 4

    @property
    def window_id(self):
        return self._miscop_get_signed(0)

    @property
    def message(self):
        return self._miscop_get_string(2)

    @message.setter
    def message(self, message):
        self._miscop_set_string(1, message)

    @property
    def title(self):
        return self._miscop_get_string(4)

    @title.setter
    def title(self, title):
        self._miscop_set_string(3, title)


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
