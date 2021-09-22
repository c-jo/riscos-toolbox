"""RISC OS Toolbox - Window"""

from . import Object
import swi

class Window(Object):
    class_id = 0x82880
    def __init__(self, id):
        super().__init__(id)
        self.gadgets = {}
        self._wimp_handle = None

    @property
    def wimp_handle(self):
        if self._wimp_handle is None:
            self._wimp_handle = swi.swi('Toolbox_ObjectMiscOp', '0I0;I',
                                        self.id)
        return self._wimp_handle

    def create_gadget(self, block, type, box, help_message=None, max_help=None):
        block.type = type
        block.min_x, block.min_y, block.max_x, block.max_y = box
        block.component_id = -1
        block.help_message, block.max_help =\
            encode_and_len(help_message, max_help)

        return swi('Toolbox_ObjectMiscOp', 'iIiI;I',
                   0, self.id, 1, ctypes.addressof(block))

    def remove_gadget(self, gadget):
        swi.swi('Toolbox_ObjectMiscOp', '0III', self.id, 2, gadget.id)

    def get_extent(self):
        extent_block = swi.block(4)
        swi.swi('Toolbox_ObjectMiscOp', '0Iib', self.id, 16, extent_block)
        return (extent_block.tosigned(0),
                extent_block.tosigned(1),
                extent_block.tosigned(2),
                extent_block.tosigned(3))

    def set_extent(self, extent):
        extent_block = swi.block(4)
        extent_block.signed(0, extent[0])
        extent_block.signed(1, extent[1])
        extent_block.signed(2, extent[2])
        extent_block.signed(3, extent[3])
        swi.swi('Toolbox_ObjectMiscOp', '0Iib', self.id, 15, extent_block)
