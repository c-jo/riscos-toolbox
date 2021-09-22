"""RISC OS Toolbox - Gadgets"""

from swi import swi
import ctypes

def encode_and_len(s, m):
    if s is None:
        return None, 0 if m is None else m
    s = s.encode('latin-1')
    return s, len(s)+1 if m is None else m

class BBox(ctypes.Structure):
    _fields_ = [("min_x", ctypes.c_int), ("min_y", ctypes.c_int),
                ("max_x", ctypes.c_int), ("max_y", ctypes.c_int)]

class Gadget:
    class Header(ctypes.Structure):
        _anonymous_ = ("box",)
        _fields_ = [("flags",        ctypes.c_uint  ),
                    ("type",         ctypes.c_uint  ),
                    ("box",          BBox           ),
                    ("component_id", ctypes.c_int   ),
                    ("help_message", ctypes.c_char_p),
                    ("max_help",     ctypes.c_uint  )]

    def __init__(self, window, id):
        self.window = window
        self.id     = id

        window.gadgets[id] = self

    def get_flags(self):
        """Gets the gadgets flags."""
        return swi('Toolbox_ObjectMiscOp','0III;I',self.window.id,64,self.id)

    def set_flags(self, flags):
        """Sets the gadgets flags."""
        swi('Toolbox_ObjectMiscOp','0IIII',self.window.id,65,self.id,flags)

    def get_flag(self, flag):
        """Gets one gadget flag."""
        return self.get_flags() & 1<<flag != 0

    def set_flag(self, flag, value):
        """Sets one gadget flag."""
        mask = 0xffffff - 1<<flag
        self.set_flags(
            self.get_flags() & mask | (1<<flag if value else 0))

    def event_handler(self, event_code, id_block, poll_block):
        pass
        #raise(RuntimeError(f'toolbox event 0x{event_code:x} not handled.'))

    @property
    def faded(self):
        return self.get_flag(31)

    @faded.setter
    def faded(self, value):
        self.set_flag(31, value)

def create(window, block, type, box, help_message=None, max_help=None):
    block.type = type
    block.min_x, block.min_y, block.max_x, block.max_y = box
    block.component_id = -1
    block.help_message, block.max_help =\
        encode_and_len(help_message, max_help)

    return swi('Toolbox_ObjectMiscOp', 'iIiI;I',
               0, window.id, 1, ctypes.addressof(block))