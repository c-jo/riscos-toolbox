"""RISC OS Toolbox - Iconbar"""

from ..base import Object
from ..events import ToolboxEvent

class Iconbar(Object):
    class_id = 0x82900
    # Events
    Clicked              = class_id + 0
    SelectAboutToBeShown = class_id + 1
    AdjustAboutToBeShown = class_id + 2

    @property
    def icon_handle(self):
        return self._miscop_get_unsigned(0)

    # Get/Set Menu
    # Get/Set Event
    # Get/Set Show

    @property
    def menu_id(self):
        return self._miscop_get_unsigned(2)

    @menu_id.setter
    def menu_id(self, id):
        return self._miscop_set__unsigned(1, id)

    @property
    def help_message(self):
        return self._miscop_get_string(8)

    @help_message.setter
    def help_message(self, message):
        self._miscop_set_string(7, message)

    @property
    def text(self):
        return self._miscop_get_string(10)

    @text.setter
    def text(self, text):
        self._miscop_set_string(9, text)

    @property
    def sprite(self):
        return self._miscop_get_string(12)

    @text.setter
    def sprite(self, name):
        self._miscop_set_string(11, name)

class ClickedEvent(ToolboxEvent):
    event_id = Iconbar.Clicked

    @property
    def select(self):
        return self.flags & 0x04 != 0

    @property
    def adjust(self):
        return self.flags & 0x01 != 0
