from . import Object

class Menu(Object):
    class_id = 0x828c0
    def __init__(self, id):
        super().__init__(id)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x828c3: # Menu_Selection
            self.menu_selection(id_block.self_component)

    def menu_selection(self, item):
        pass