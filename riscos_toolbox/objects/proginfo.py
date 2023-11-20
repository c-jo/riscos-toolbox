"""RISC OS Toolbox - ProgInfo"""

from ..base import Object
from ..events import AboutToBeShownEvent, ToolboxEvent
from enum import IntEnum


class ProgInfo(Object):
    class_id = 0x82b40
    # Methods
    GetWindowId = 0
    SetVersion = 1
    GetVersion = 2
    SetLicenceType = 3
    GetLicenceType = 4
    SetTitle = 5
    GetTitle = 6
    SetUri = 7
    GetUri = 8
    SetWebEvent = 9
    GetWebEvent = 10
    # Events
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    LaunchWebPage     = class_id + 2

    LicenceType = IntEnum(
        "LicenceType",
        "Unset PublicDomain SingleUser SingleMachine Site Network Authority".split(),
        start=-1)

    @property
    def window_id(self):
        return self._miscop_get_unsigned(ProgInfo.GetWindowId)

    @property
    def version(self):
        return self._miscop_get_string(ProgInfo.GetVersion)

    @version.setter
    def version(self, version):
        self._miscop_set_string(ProgInfo.SetVersion, version)

    @property
    def licence_type(self):
        return ProgInfo.LicenceType(self._miscop_get_signed(ProgInfo.GetLicenceType))

    @licence_type.setter
    def licence_type(self, licence_type):
        self._miscop_set_signed(ProgInfo.SetLicenceType, licence_type)

    @property
    def title(self):
        return self._miscop_get_string(ProgInfo.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(ProgInfo.SetTitle, title)

    @property
    def uri(self):
        return self._miscop_get_string(ProgInfo.GetUri)

    @uri.setter
    def uri(self, uri):
        self._miscop_set_string(ProgInfo.SetUri, uri)

    @property
    def web_event(self):
        return self._miscop_get_unsigned(ProgInfo.GetWebEvent)

    @web_event.setter
    def web_event(self, web_event):
        self._miscop_set_unsigned(ProgInfo.SetWebEvent, web_event)


class ProgInfoAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = ProgInfo.AboutToBeShown


class ProgInfoDialogueCompletedEvent(ToolboxEvent):
    event_id = ProgInfo.DialogueCompleted


class ProgInfoLaunchWebPageEvent(ToolboxEvent):
    event_id = ProgInfo.LaunchWebPage
