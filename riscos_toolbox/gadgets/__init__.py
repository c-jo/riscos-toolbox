"""RISC OS Toolbox - Gadgets"""

import swi
import ctypes

from .._types import BBox, ComponentID
from ..base import Component

_gadgets = {}  # type -> class


def encode_and_len(s, m):
    if s is None:
        return None, 0 if m is None else m
    s = s.encode('latin-1')
    return s, len(s) + 1 if m is None else m


class Gadget(Component):
    _type = None

    def __subclass_init__(self, cls):
        if cls._type is not None:
            _gadgets[cls._type] = cls

    def __init__(self, window, id):
        super().__init(id)
        self.window = window
        self.id = id
        window.components[id] = self

    @staticmethod
    def create(gadget_type, window, gadget_id):
        return _gadgets[gadget_type](window, gadget_id)

    @property
    def flags(self):
        """Gets the gadgets flags."""
        return swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.window.id, 64, self.id)

    @flags.setter
    def flags(self, flags):
        """Sets the gadgets flags."""
        swi.swi('Toolbox_ObjectMiscOp', '0IIII', self.window.id, 65, self.id, flags)

    def get_flag(self, flag):
        """Gets one gadget flag."""
        return self.get_flags() & 1 << flag != 0

    def set_flag(self, flag, value):
        """Sets one gadget flag."""
        mask = ~ (1 << flag)
        self.flags = self.flags & mask | (1 << flag if value else 0)

    @property
    def faded(self):
        return self.get_flag(31)

    @faded.setter
    def faded(self, value):
        self.set_flag(31, value)

    # Wrappers for Toolbox_ObjectMiscOp for some common cases
    def _miscop_set_signed(self, op, value, flags=0):
        """Use Toolbox_ObjectMiscOp to set an unsigned integer."""
        swi.swi('Toolbox_ObjectMiscOp', 'IIIIi',
                flags, self.window.id, op, self.id, value)

    def _miscop_get_signed(self, op, flags=0):
        """Use Toolbox_ObjectMiscOp to get an unsigned integer."""
        return swi.swi('Toolbox_ObjectMiscOp', 'IIII;i',
                       flags, self.window.id, op, self.id)

    def _miscop_set_unsigned(self, op, value, flags=0):
        """Use Toolbox_ObjectMiscOp to set an unsigned integer."""
        swi.swi('Toolbox_ObjectMiscOp', 'IIIII',
                flags, self.window.id, op, self.id, value)

    def _miscop_get_unsigned(self, op, flags=0):
        """Use Toolbox_ObjectMiscOp to get an unsigned integer."""
        return swi.swi('Toolbox_ObjectMiscOp', 'IIII;I',
                       flags, self.window.id, op, self.id)

    def _miscop_set_string(self, op, text, flags=0):
        """Use Toolbox_ObjectMiscOp to set a string."""
        swi.swi('Toolbox_ObjectMiscOp', 'IIIis',
                flags, self.window.id, op, self.id, text)

    def _miscop_get_string(self, op, flags=0):
        """Use Toolbox_ObjectMiscOp to get a string. This call will allocate
           a suitably-sized buffer, read the string and return it."""
        buf_size = swi.swi('Toolbox_ObjectMiscOp', 'IIII00;.....I',
                           flags, self.window.id, op, self.id)
        buffer = swi.block((buf_size + 3) // 4)
        swi.swi('Toolbox_ObjectMiscOp', 'IIIibI',
                flags, self.window.id, op, self.id, buffer, buf_size)
        return buffer.nullstring()

    def _miscop_set_font(self, op, name, width=None, height=None, size=None):
        """Use Toolbox_ObjectMiscOp to set a font. Specify the font name and
           height and width or size (in points). Specifing height, with and size
           will result in size value being ignored. If font name is None, the
           system font will be used."""
        if width is None and height is None and size:
            width = height = size

        if width is None or height is None:
            raise ValueError("Font height and width or size must be specified.")

        if name:
            swi.swi('Toolbox_ObjectMiscOp', 'IIIIsii',
                    0, self.window.id, op, self.id,
                    name, int(width * 16), int(height * 16))
        else:
            swi.swi('Toolbox_ObjectMiscOp', 'IIII0ii',
                    0, self.window.id, op, self.id,
                    int(width * 16), int(height * 16))


class GadgetDefinition(ctypes.Structure):
    _fields_ = [
        ('flags', ctypes.c_int32),
        ('type', ctypes.c_int32),
        ('box', BBox),
        ('component_id', ComponentID),
        ('help_message', ctypes.c_char_p),
        ('max_help', ctypes.c_int32)
    ]

    def __init__(self, flags, type, box, component_id=-1,
                 help_message=None, max_help=None):
        self.flags = flags
        self.type = type
        self.box = box
        self.component_id = component_id
        self.help_message, self.max_help = encode_and_len(help_message, max_help)
