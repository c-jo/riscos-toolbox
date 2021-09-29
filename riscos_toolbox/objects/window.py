"""RISC OS Toolbox - Window"""

from .. import Object
import swi

class Window(Object):
    class_id = 0x82880
    def __init__(self, id):
        super().__init__(id)
        self.gadgets = self.components
        self._wimp_handle = None

    @property
    def wimp_handle(self):
        if self._wimp_handle is None:
            self._wimp_handle = swi.swi('Toolbox_ObjectMiscOp', '0II;I',
                                        self.id, 0)
        return self._wimp_handle

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II0;....I', self.id, 12)
        buffer = swi.block(int((buf_size+3)/4))
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI', self.id, 12,
                                                 buffer, buf_size)
        return buffer.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs', self.id, 11, title)

    def add_gadget(self, block, klass):
        id = swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.id, 1, block)
        obj = klass(self, id)
        self.gadgets[id] = obj
        return obj

    def remove_gadget(self, gadget):
        swi.swi('Toolbox_ObjectMiscOp', '0III', self.id, 2, gadget.id)
        del self.gadgets[gadget.id]

    @property
    def extent(self):
        extent_block = swi.block(4)
        swi.swi('Toolbox_ObjectMiscOp', '0Iib', self.id, 16, extent_block)
        return (extent_block.tosigned(0),
                extent_block.tosigned(1),
                extent_block.tosigned(2),
                extent_block.tosigned(3))

    @extent.setter
    def extent(self, extent):
        extent_block = swi.block(4)
        extent_block.signed(0, extent[0])
        extent_block.signed(1, extent[1])
        extent_block.signed(2, extent[2])
        extent_block.signed(3, extent[3])
        swi.swi('Toolbox_ObjectMiscOp', '0Iib', self.id, 15, extent_block)
