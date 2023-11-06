"""RISC OS Toolbox - ProgInfo"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
from enum import IntEnum


class ProgInfo(Object):
    class_id = 0x82b40

    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    LaunchWebPage     = class_id + 2

    LicenceType = IntEnum(
        "LicenceType",
        "PublicDomain SingleUser SingleMachine Site Network Authority".split(),
        start=0)

    @property
    def window_id(self):
        return self._miscop_get_signed(0)

    @property
    def version(self):
        return self._miscop_get_string(2)

    @version.setter
    def version(self, version):
        self._miscop_set_string(1, version)

    @property
    def licence_type(self):
        return ProgInfo.LicenceType(self._miscop_get_unsigned(4))

    @licence_type.setter
    def license_type(self, licence_type):
        self._miscop_set_signed(3, licence_type)

    @property
    def title(self):
        return self._miscop_get_string(6)

    @title.setter
    def title(self, title):
        self._miscop_set_string(5, title)

    @property
    def uri(self):
        return self._miscop_get_string(8)

    @uri.setter
    def uri(self, uri):
        self._miscop_set_string(7, uri)

    @property
    def web_event(self):
        return self._miscop_get_unsigned(10)

    @web_event.setter
    def web_event(self, web_event):
        self._miscop_set_unsigned(9, web_event)


# ProgInfo Events
class ProgInfoAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = ProgInfo.AboutToBeShown


class ProgInfoDialogueCompletedEvent(ToolboxEvent):
    event_id = ProgInfo.DialogueCompleted


class ProgInfoLaunchWebPageEvent(ToolboxEvent):
    event_id = ProgInfo.LaunchWebPage
