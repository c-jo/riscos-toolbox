"""RISC OS Toolbox - Gadgets"""

import swi
import ctypes

def encode_and_len(s, m):
    if s is None:
        return None, 0 if m is None else m
    s = s.encode('latin-1')
    return s, len(s)+1 if m is None else m

class Point(ctypes.Structure):
    _fields_ = [ ("x", ctypes.c_int), ("y", ctypes.c_int) ]

class BBox(ctypes.Structure):
    _fields_ = [ ("min", Point ), ("max", Point) ]

class Gadget:
    class Header(ctypes.Structure):
        _anonymous_ = ("box",)
        _fields_ = [("flags",        ctypes.c_uint  ),
                    ("type",         ctypes.c_uint  ),
                    ("box",          BBox           ),
                    ("component_id", ctypes.c_int   ),
                    ("help_message", ctypes.c_char_p),
                    ("max_help",     ctypes.c_uint  )]

        def __init__(self, flags, type, box, component_id=-1,
                           help_message=None, max_help=None):
            self.flags = flags
            self.type  = type
            self.min.x, self.min.y, self.max.x, self.max.y = box
            self.component_id = component_id
            self.help_message,self.max_help = encode_and_len(help_message,max_help)

    def __init__(self, window, id):
        self.window = window
        self.id     = id

        window.gadgets[id] = self

    @property
    def flags(self):
        """Gets the gadgets flags."""
        return swi.swi('Toolbox_ObjectMiscOp','0III;I',self.window.id,64,self.id)

    @flags.setter
    def flags(self, flags):
        """Sets the gadgets flags."""
        swi.swi('Toolbox_ObjectMiscOp','0IIII',self.window.id,65,self.id,flags)

    def get_flag(self, flag):
        """Gets one gadget flag."""
        return self.get_flags() & 1<<flag != 0

    def set_flag(self, flag, value):
        """Sets one gadget flag."""
        mask = ~(1<<flag)
        self.flags = self.flags & mask | (1<<flag if value else 0)

    def event_handler(self, event_code, id_block, poll_block):
        pass
        #raise(RuntimeError(f'toolbox event 0x{event_code:x} not handled.'))

    @property
    def faded(self):
        return self.get_flag(31)

    @faded.setter
    def faded(self, value):
        self.set_flag(31, value)

    def _miscop_set_int(self, op, value):
        """Use Toolbox_ObjectMiscOp to set an integer."""
        swi.swi('Toolbox_ObjectMiscOp', '0IIII',
                self.window.id,op,self.id,value)

    def _miscop_get_int(self, op):
        """Use Toolbox_ObjectMiscOp to get an integer."""
        return swi.swi('Toolbox_ObjectMiscOp', '0III:I',
                       self.window.id,op,self.id,value)

    def _miscop_set_text(self, op, text):
        """Use Toolbox_ObjectMiscOp to set a string."""
        swi.swi('Toolbox_ObjectMiscOp', '0IIIs',
                           self.window.id,op,self.id,text)

    def _miscop_get_text(self, op):
        """Use Toolbox_ObjectMiscOp to get a string. This call will allocate
           a suitably-sized buffer, read the string and return it."""
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0IIII00;....I',
                           self.window.id,op,self.id)
        buffer = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIIIbI',
                           self.window.id,op,self.id,buffer,buf_size)
        return block.nullstring()

