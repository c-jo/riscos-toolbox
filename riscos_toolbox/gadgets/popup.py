# Module implementing the Toolbox's PopUp gadget.

import ctypes
from riscos_toolbox.gadgets import Gadget, GadgetDefinition
from riscos_toolbox.events import ToolboxEvent

class PopUp(Gadget):
    _type = 704

    # Methods
    SetMenu = _type + 0
    GetMenu = _type + 1

    # Events
    AboutToBeShown = 0x8288B # Window SWI chunk base (0x82880) + 11

    # Flags
    GenerateAboutToBeShown = 0x00000001

    @property
    def menu(self):
        return self._miscop_get_int(self.GetMenu)

    @menu.setter
    def menu(self,id):
        self._miscop_set_int(self.SetMenu,id)

class PopUpDefinition(GadgetDefinition):
    _gadget_class = PopUp
    _fields_ = [ ("menu",ctypes.c_char_p) ]

class PopUpAboutToBeShownEvent(ToolboxEvent):
    event_id = PopUp.AboutToBeShown

    # There's extra fields in the header that aren't in the documentation,
    # but these aren't implemented here.
    _fields_ = [ ("_menu_id",ctypes.c_int32) ]

    @property
    def menu_id(self):
        return self._menu_id

