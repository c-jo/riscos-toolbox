from ..base import Object
from ..events import ToolboxEvent, AboutToBeShownEvent
from .. import Point

from collections import namedtuple
import ctypes
import swi


ClickShow = namedtuple("ClickShow", "object_id transient")


class Menu(Object):
    class_id = 0x828c0
    # Methods
    SetTick             = 0
    GetTick             = 1
    SetFade             = 2
    GetFade             = 3
    SetEntryText        = 4
    GetEntryText        = 5
    SetEntrySprite      = 6
    GetEntrySprite      = 7
    SetSubMenuShow      = 8
    GetSubMenuShow      = 9
    SetSubMenuEvent     = 10
    GetSubMenuEvent     = 11
    SetClickShow        = 12
    GetClickShow        = 13
    SetClickEvent       = 14
    GetClickEvent       = 15
    SetHelpMessage      = 16
    GetHelpMessage      = 17
    SetEntryHelpMessage = 18
    GetEntryHelpMessage = 19
    AddEntry            = 20
    RemoveEntry         = 21
    GetHeight           = 22
    GetWidth            = 23
    SetTitle            = 24
    GetTitle            = 25
    # Events
    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1
    SubMenu        = class_id + 2
    Selection      = class_id + 3
    # Constants
    AddEntryBefore      = 0x00000001
    AddEntryAtBeginning = -1
    AddEntryAtEnd       = -2
    GenerateShowEvent = 0x00000001
    GenerateHideEvent = 0x00000002

    class MenuTemplateEntry(ctypes.Structure):
        _fields_ = [
            ("flags", ctypes.c_uint32),
            ("component", ctypes.c_uint32),
            ("text", ctypes.c_char_p),
            ("max_text", ctypes.c_uint32),
            ("click_show", ctypes.c_char_p),
            ("submenu_show", ctypes.c_char_p),
            ("submenu_event", ctypes.c_uint32),
            ("click_event", ctypes.c_uint32),
            ("help_message", ctypes.c_char_p),
            ("max_help", ctypes.c_uint32),
        ]

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
        Ticked = 0x00000001
        DottedLine = 0x00000002
        Faded = 0x00000100
        IsSprite = 0x00000200
        SubMenu = 0x00000400
        GenerateSubMenuEvent = 0x00000800
        ClickShowTransient = 0x00001000

        def __init__(self, menu, id):
            self.menu = menu
            self.id = id

        def _miscop_get_signed(self, op):
            return swi.swi('Toolbox_ObjectMiscOp', 'IiIi;i',
                           0, self.menu.id, op, self.id)

        def _miscop_set_signed(self, op, value):
            return swi.swi('Toolbox_ObjectMiscOp', 'IiIii',
                           0, self.menu.id, op, self.id, value)

        def _miscop_get_unsigned(self, op):
            return swi.swi('Toolbox_ObjectMiscOp', 'IiIi;I',
                           0, self.menu.id, op, self.id)

        def _miscop_set_unsigned(self, op, value):
            return swi.swi('Toolbox_ObjectMiscOp', 'IiIiI',
                           0, self.menu.id, op, self.id, value)

        def _miscop_get_string(self, op):
            buf_size = swi.swi('Toolbox_ObjectMiscOp', 'IiIi00;.....i',
                               0, self.menu.id, op, self.id)
            buf = swi.block((buf_size + 3) // 4)
            swi.swi('Toolbox_ObjectMiscOp', 'IiIibi',
                    0, self.menu.id, op, self.id, buf, buf_size)
            return buf.nullstring()

        def _miscop_set_string(self, op, value):
            swi.swi('Toolbox_ObjectMiscOp', 'IiIis', value)

        @property
        def tick(self):
            return self._miscop_get_unsigned(Menu.GetTick) != 0

        @tick.setter
        def tick(self, tick):
            self._miscop_set_unsigned(Menu.SetTick, 1 if tick else 0)

        @property
        def fade(self):
            return self._miscop_get_unsigned(Menu.GetFade) != 0

        @fade.setter
        def fade(self, fade):
            self._miscop_set_unsigned(Menu.SetFade, 1 if fade else 0)

        @property
        def text(self):
            return self._miscop_get_string(Menu.GetEntryText)

        @text.setter
        def text(self, text):
            self._miscop_set_string(Menu.SetEntryText, text)

        @property
        def sprite(self):
            return self._miscop_get_string(Menu.GetEntrySprite)

        @sprite.setter
        def sprite(self, sprite):
            self._miscop_set_string(Menu.SetEntrySprite, sprite)

        @property
        def submenu_show(self):
            return self._miscop_get_unsigned(Menu.GetSubMenuShow)

        @submenu_show.setter
        def submenu_show(self, submenu_show):
            return self._miscop_set_unsigned(Menu.SetSubMenuShow, submenu_show)

        @property
        def submenu_event(self):
            return self._miscop_get_unsigned(Menu.GetSubMenuEvent)

        @submenu_event.setter
        def submenu_event(self, submenu_event):
            return self._miscop_set_signed(Menu.SetSubMenuShow, submenu_event)

        @property
        def click_show(self):
            object_id, flags = swi.swi('Toolbox_ObjectMiscOp', 'IiIi;ii',
                                       0, self.menu.id, Menu.GetClickShow, self.id)
            return ClickShow(object_id, flags & Menu.Entry.ClickShowTransient != 0)

        @click_show.setter
        def click_show(self, click_show):
            if isinstance(click_show, int):
                click_show = ClickShow(click_show, False)
            swi.swi('Toolbox_ObjectMiscOp', 'IiIiii',
                    0, self.menu.id, Menu.SetClickShow, self.id, click_show.object_id,
                    Menu.Entry.ClickShowTransient if click_show.transient else 0)

        @property
        def click_event(self):
            return self._miscop_get_unsigned(Menu.GetClickEvent)

        @click_event.setter
        def click_event(self, click_event):
            self._miscop_set_signed(Menu.SetClickEvent, click_event)

        @property
        def help_message(self):
            return self._miscop_get_string(Menu.GetEntryHelpMessage)

        @help_message.setter
        def help_message(self, help_message):
            self._miscop_set_string(Menu.SetEntryHelpMessage, help_message)

    def __getitem__(self, id):
        return Menu.Entry(self, id)

    @property
    def help_message(self):
        return self._miscop_get_string(Menu.GetHelpMessage)

    @help_message.setter
    def help_message(self, help_message):
        self._miscop_set_string(Menu.SetHelpMessage, help_message)

    def _add(self,
             flags, where, component, text,
             click_show=None, submenu_show=None,
             submenu_event=None, click_event=None,
             help_message=None):
        details = Menu.MenuTemplateEntry(component)
        text_buffer = ctypes.create_string_buffer(text.encode("latin-1"))
        details.text = ctypes.addressof(text_buffer)
        details.max_text = len(details.text) + 1
        if click_event:
            details.click_event = click_event

        return swi.swi('Toolbox_ObjectMiscOp', 'IiIiI;i',
                       flags, self.id, Menu.AddEntry, where, ctypes.addressof(details))

    def add_at_end(self, *args, **kwargs):
        self._add(0, Menu.AddEntryAtEnd, *args, **kwargs)

    def add_at_beginning(self, *args, **kwargs):
        self._add(0, Menu.AddEntryAtBeginning, *args, **kwargs)

    def add_before(self, before, *args, **kwargs):
        self._add(Menu.AddEntryBefore, before, *args, **kwargs)

    def add_after(self, after, *args, **kwargs):
        self._add(0, after, *args, **kwargs)

    def remove(self, component):
        swi.swi("Toolbox_ObjectMiscOp", "IIII", 0, self.id, Menu.RemoveEntry, component)

    @property
    def height(self):
        return self._miscop_get_signed(Menu.GetHeight)

    @property
    def width(self):
        return self._miscop_get_signed(Menu.GetWidth)

    @property
    def title(self):
        return self._miscop_get_string(Menu.GetTitle)

    @title.setter
    def title(self, title):
        self._miscop_set_string(Menu.SetTitle, title)


class MenuAboutToBeShownEvent(AboutToBeShownEvent):
    event_id = Menu.AboutToBeShown


class MenuHasBeenHiddenEvent(ToolboxEvent):
    event_id = Menu.HasBeenHidden


class MenuSubMenuEvent(ToolboxEvent):
    event_id = Menu.SubMenu
    _fields_ = [("pos", Point)]


class SelectionEvent(ToolboxEvent):
    event_id = Menu.Selection
