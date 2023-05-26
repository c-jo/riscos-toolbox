from ..base import Object
from ..events import ToolboxEvent

import ctypes
import swi

class Menu(Object):
    class_id = 0x828c0

    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1
    SubMenu        = class_id + 2
    Selection      = class_id + 3

    class MenuTemplateEntry(ctypes.Structure):
        _fields_ = [ ("flags", ctypes.c_uint32),
                     ("component", ctypes.c_uint32),
                     ("text", ctypes.c_char_p),
                     ("max_text", ctypes.c_uint32),
                     ("click_show", ctypes.c_char_p),
                     ("submenu_show", ctypes.c_char_p),
                     ("submenu_event", ctypes.c_uint32),
                     ("click_event", ctypes.c_uint32),
                     ("help_message", ctypes.c_char_p),
                     ("max_help", ctypes.c_uint32) ]

        def __init__(self, component):
            self.flags = 0
            self.component = component
            self.text = 0
            self.max_text = 0
            self.click_show = 0
            self.submenu_show = 0
            self.submenu_event = 0
            self.click_event = 0
            self.help_message = 0
            self.max_help = 0

    class Entry:
        def __init__(self, menu, id):
            self.menu = menu
            self.id = id

        @property
        def tick(self):
            return swi.swi('Toolbox_ObjectMiscOp','0II;I',
                           self.menu.id, 1, self.id) != 0

        @tick.setter
        def tick(self, val):
            swi.swi('Toolbox_ObjectMiscOp','0IIII',
                    self.menu.id, 0, self.id, 1 if val else 0)

        @property
        def fade(self):
            return swi.swi('Toolbox_ObjectMiscOp','0II;I',
                           self.menu.id, 3, self.id) != 0

        @fade.setter
        def fade(self, val):
            swi.swi('Toolbox_ObjectMiscOp','0IIII',
                    self.menu.id, 2, self.id, 1 if val else 0)

    def __getitem__(self, id):
        return Menu.Entry(self, id)

    def add_at_end(self, component, text,
                   click_show=None, submenu_show=None,
                   submenu_event=None,click_event=None,
                   help_message=None):
        flags = 0
        details = Menu.MenuTemplateEntry(component)
        text_buffer = ctypes.create_string_buffer(text.encode("latin-1"))

        details.text = ctypes.addressof(text_buffer)
        details.max_text = len(details.text)+1
        if click_event:
            details.click_event = click_event

        return swi.swi('Toolbox_ObjectMiscOp','IIIiI;I',
                flags, self.id, 20, -1, ctypes.addressof(details))

    def remove(self, component):
        swi.swi("Toolbox_ObjectMiscOp","IIII", 0, self.id, 21, component)

class SelectionEvent(ToolboxEvent):
    event_id = Menu.Selection
