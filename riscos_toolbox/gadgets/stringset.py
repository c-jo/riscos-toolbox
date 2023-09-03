# Module implementing the Toolbox's StringSet gadget.

import ctypes
import swi
from riscos_toolbox.gadgets import Gadget, GadgetDefinition
from riscos_toolbox.events import ToolboxEvent

class StringSet(Gadget):
    _type = 896

    # Methods
    SetAvailable  = _type + 0
    SetSelected   = _type + 2
    GetSelected   = _type + 3
    SetAllowable  = _type + 4
    GetComponents = _type + 6
    SetFont       = _type + 7

    # Events
    ValueChanged   = 0x8288E # Window SWI chunk base + 14
    AboutToBeShown = 0x8288F # Window SWI chunk base + 15

    # Flags
    GenerateUserValueChanged = 0x00000001
    GenerateSetValueChanged  = 0x00000002
    Writable                 = 0x00000004
    GenerateAboutToBeShown   = 0x00000008
    NoDisplay                = 0x00000010
    # Flags - GetComponents
    ReturnAlphaNumericField  = 0x00000001
    ReturnPopUpMenu          = 0x00000002
    # Method constants
    IndexedSelection         = 0x00000001

    # There are two ways to set the selected; by string or by index.
    # After some consideration, the solution that made the most sense was to
    # break this into two properties.
    @property
    def selected(self):
        # Thankfully flags=0 means return string, so _miscop_get_text works
        return self._miscop_get_text(StringSet.GetSelected)

    @selected.setter
    def selected(self,selection):
        self._miscop_set_text(StringSet.SetSelected,selection)

    @property
    def index(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;i',StringSet.IndexedSelection,
                       self.window.id,StringSet.GetSelected,self.id)

    @index.setter
    def index(self,index):
        swi.swi('Toolbox_ObjectMiscOp','IiiiI',StringSet.IndexedSelection,
                self.window.id,StringSet.SetSelected,self.id,index)

    # Here are some read-only properties for the components making up the StringSet,
    # which have been split out from GetComponents
    @property
    def alphanumeric_field(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;i',StringSet.ReturnAlphaNumericField,
                       self.window.id,StringSet.GetComponents,self.id)

    @property
    def popup_menu(self):
        return swi.swi('Toolbox_ObjectMiscOp','Iiii;.i',StringSet.ReturnPopUpMenu,
                       self.window.id,StringSet.GetComponents,self.id)

    def set_available(self,items):
        self._miscop_set_text(StringSet.SetAvailable,items)

    def set_allowable(self,allowable):
        self._miscop_set_text(StringSet.SetAllowable,allowable)

    def set_font(self,name,width,height):
        swi.swi('Toolbox_ObjectMiscOp','0iiisII',self.window.id,StringSet.SetFont,
                self.id,name,width,height)

class StringSetDefinition(GadgetDefinition):
    _gadget_class = StringSet
    _fields_ = [ ("string_set",ctypes.c_char_p),
                 ("title",ctypes.c_char_p),
                 ("initial_selected_string",ctypes.c_char_p),
                 ("max_selected_string_len",ctypes.c_int32),
                 ("allowable",ctypes.c_char_p),
                 ("max_allowable_len",ctypes.c_int32),
                 ("before",ctypes.c_int32),
                 ("after",ctypes.c_int32) ]

class StringSetValueChangedEvent(ToolboxEvent):
    event_id = StringSet.ValueChanged

    _fields_ = [ ("_new_string",ctypes.c_char * 212) ]

    @property
    def new_string(self):
        return self._new_string.decode("latin-1")

class StringSetAboutToBeShownEvent(ToolboxEvent):
    event_id = StringSet.AboutToBeShown

    # No fields
