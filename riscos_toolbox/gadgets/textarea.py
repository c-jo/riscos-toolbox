# Module implementing the Toolbox's TextArea gadget.

import swi
import ctypes
from riscos_toolbox.gadgets import Gadget, GadgetDefinition

class TextArea(Gadget):
    _type = 0x4018 # from TextArea_Base

    # Methods
    GetState          = _type + 0
    SetState          = _type + 1
    SetText           = _type + 2
    GetText           = _type + 3
    InsertText        = _type + 4
    ReplaceText       = _type + 5
    GetSelection      = _type + 6
    SetSelection      = _type + 7
    SetFont           = _type + 8
    SetColour         = _type + 9
    GetColour         = _type + 10
    SetCursorPosition = _type + 11
    GetCursorPosition = _type + 12

    # This gadget has no events.

    # Flags
    Scrollbar_Vertical   = 0x00000001
    Scrollbar_Horizontal = 0x00000002
    WordWrap             = 0x00000004
    ValidFlags           = 0xC0000007

    @property
    def state(self):
        return self._miscop_get_int(TextArea.GetState)

    @state.setter
    def state(self, state):
        self._miscop_set_int(TextArea.SetState,state)

    @property
    def text(self):
        return self._miscop_get_text(TextArea.GetText)

    @text.setter
    def text(self, text):
        self._miscop_set_text(TextArea.SetText,text)

    # GetSelection and SetSelection work siimilarly to StringSet's, but the flags are
    # backwards, meaning bit 0 set is return string and bit 0 clear is return text.
    # These two usages have been split into two properties, selection_points for the indices
    # and selection for the text itself.

    # Returns a tuple containing a start and end index.
    @property
    def selection_points(self):
        return swi.swi('Toolbox_ObjectMiscOp','0iii;....ii',self.window.id,
                       TextArea.GetSelection,self.id)

    # This setter takes a tuple containing a start and end index.
    @selection_points.setter
    def selection_points(self, indexes):
        start, end = indexes
        swi.swi('Toolbox_ObjectMiscOp','0iiiII',self.window.id,TextArea.SetSelection,
                self.id,start,end)

    # No matter what, this seems to return 1 character past where it should;
    # This was tested with the C veneer and had the same behavior, so it appears
    # to be a quirk or bug with the Toolbox itself. Otherwise, it is harmless as
    # selecting the whole text causes no problems.
    @property
    def selection(self):
        bufsize = swi.swi('Toolbox_ObjectMiscOp','1iii0;.....I',self.window.id,
                          TextArea.GetSelection,self.id)
        buf = swi.block((bufsize+3)//4)
        swi.swi('Toolbox_ObjectMiscOp','1iiibi',self.window.id,TextArea.GetSelection,
                self.id,buf,bufsize)
        return buf.nullstring()

    # This one just replaces the text according to the selection points
    @selection.setter
    def selection(self,text):
        start, end = self.selection_points
        self.replace(start,end,text)

    @property
    def cursor(self):
        return swi.swi('Toolbox_ObjectMiscOp','0iii;....i',self.window.id,
                       TextArea.GetCursorPosition,self.id)

    @cursor.setter
    def cursor(self, pos):
        self._miscop_set_int(TextArea.SetCursorPosition, pos)

    # This returns a tuple containing (foreground, background)
    @property
    def colour(self):
        return swi.swi('Toolbox_ObjectMiscOp','0iii;II',self.window.id,
                       TextArea.GetColour,self.id)

    # This one takes a tuple containing (foreground, background)
    @colour.setter
    def colour(self,colour):
        fg, bg = colour
        swi.swi('Toolbox_ObjectMiscOp','0iiiII',self.window.id,
                TextArea.SetColour,self.id,fg,bg)

    # Insert text at a specified offset
    def insert(self, index, text):
        swi.swi('Toolbox_ObjectMiscOp','0iiiis',self.window.id,TextArea.InsertText,
                self.id,index,text)

    # Replace a block of text with new text
    def replace(self, start, end, text):
        swi.swi('Toolbox_ObjectMiscOp','0iiiIIs',self.window.id,TextArea.ReplaceText,
                self.id,start,end,text)

    def set_font(self, name, width, height):
        swi.swi('Toolbox_ObjectMiscOp','0iiisII',self.window.id,TextArea.SetFont,
                self.id,name,width,height)


class TextAreaDefinition(GadgetDefinition):
    _gadget_class = TextArea
    _fields_ = [ ("type", ctypes.c_int32),
                 ("event", ctypes.c_int32),
                 ("text", ctypes.c_char_p),
                 ("foreground", ctypes.c_uint32),
                 ("background", ctypes.c_uint32) ]
