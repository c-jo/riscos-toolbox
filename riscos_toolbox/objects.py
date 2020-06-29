"""RISC OS Toolbox - Objects"""

class Object:
    class_id  = None
    name      = None
    _classes  = {} # (ID,Name) -> Class

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

class Window(Object):
    class_id = 0x82880
    def __init__(self, id):
        super().__init__(id)
        self.gadgets = {}

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