"""RISC OS Toolbox - Objects"""

import swi

class Object:
    class_id  = None
    name      = None
    _classes  = {} # (Class ID,Name) -> Class

    def __init__(self, id):
        self.id = id

    def __init_subclass__(subclass):
        Object._classes[(subclass.class_id, subclass.name)] = subclass

    @staticmethod
    def create(class_id, name, id):
        if (class_id,name) in Object._classes:
            return Object._classes[(class_id,name)](id)
        if (class_id,None) in Object._classes:
            return Object._classes[(class_id,None)](id)
        else:
            return Object(id)

    def event_handler(self, event_code, id_block, poll_block):
        pass

    def wimp_handler(self, reason, id_block, poll_block):
        pass

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


class ProgInfo(Object):
    class_id = 0x82b40
    def __init__(self, id):
        super().__init__(id)

class Menu(Object):
    class_id = 0x828c0
    def __init__(self, id):
        super().__init__(id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x828c3: # Menu_Selection
            self.menu_selection(id_block.self_component)

    def menu_selection(self, item):
        pass