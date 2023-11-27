"""RISC OS Toolbox - Iconbar"""
import swi

from ..base import Object
from ..events import ToolboxEvent


class Iconbar(Object):
    class_id = 0x82900
    # Methods
    GetIconHandle  = 0
    SetMenu        = 1
    GetMenu        = 2
    SetEvent       = 3
    GetEvent       = 4
    SetShow        = 5
    GetShow        = 6
    SetHelpMessage = 7
    GetHelpMessage = 8
    SetText        = 9
    GetText        = 10
    SetSprite      = 11
    GetSprite      = 12
    # Events
    Clicked              = class_id + 0
    SelectAboutToBeShown = class_id + 1
    AdjustAboutToBeShown = class_id + 2
    # Constants
    SetEvent_Select = 0x00000001
    SetEvent_Adjust = 0x00000002
    SetShow_Select  = 0x00000001
    SetShow_Adjust  = 0x00000002

    @property
    def icon_handle(self):
        return self._miscop_get_signed(Iconbar.GetIconHandle)

    @property
    def menu_id(self):
        return self._miscop_get_unsigned(Iconbar.GetMenu)

    @menu_id.setter
    def menu_id(self, id):
        return self._miscop_set_unsigned(Iconbar.SetMenu, id)

    @property
    def select_event(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiI;i.',
                       0, self.id, Iconbar.GetEvent)

    @select_event.setter
    def select_event(self, id):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIi0',
                Iconbar.SetEvent_Select, self.id, Iconbar.SetEvent, id)

    @property
    def adjust_event(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiI;.i',
                       0, self.id, Iconbar.GetEvent)

    @adjust_event.setter
    def adjust_event(self, id):
        swi.swi('Toolbox_ObjectMiscOp', 'IiI0i',
                Iconbar.SetEvent_Adjust, self.id, Iconbar.SetEvent, id)

    @property
    def show_select_id(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiI;i.',
                       0, self.id, Iconbar.GetShow)

    @show_select_id.setter
    def show_select_id(self, id):
        swi.swi('Toolbox_ObjectMiscOp', 'IiIi0',
                Iconbar.SetShow_Select, self.id, Iconbar.SetShow, id)

    @property
    def show_adjust_id(self):
        return swi.swi('Toolbox_ObjectMiscOp', 'IiI;.i',
                       0, self.id, Iconbar.GetShow)

    @show_adjust_id.setter
    def show_adjust_id(self, id):
        swi.swi('Toolbox_ObjectMiscOp', 'Ii0i',
                Iconbar.SetShow_Adjust, self.id, Iconbar.SetShow, id)

    @property
    def help_message(self):
        return self._miscop_get_string(Iconbar.GetHelpMessage)

    @help_message.setter
    def help_message(self, message):
        self._miscop_set_string(Iconbar.SetHelpMessage, message)

    @property
    def text(self):
        return self._miscop_get_string(Iconbar.GetText)

    @text.setter
    def text(self, text):
        self._miscop_set_string(Iconbar.SetText, text)

    @property
    def sprite(self):
        return self._miscop_get_string(Iconbar.GetSprite)

    @sprite.setter
    def sprite(self, name):
        self._miscop_set_string(Iconbar.SetSprite, name)


# Iconbar Events
class IconbarClickedEvent(ToolboxEvent):
    event_id = Iconbar.Clicked
    Clicked_Adjust = 0x00000001
    Clicked_Select = 0x00000004

    @property
    def select(self):
        return self.flags & IconbarClickedEvent.Clicked_Select != 0

    @property
    def adjust(self):
        return self.flags & IconbarClickedEvent.Clicked_Adjust != 0


# For compatability with 1.0.2 and below
ClickedEvent = IconbarClickedEvent
