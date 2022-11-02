from .. import Object
import swi

class Menu(Object):
    class_id = 0x828c0

    AboutToBeShown = class_id + 0
    HasBeenHidden  = class_id + 1
    SubMenu        = class_id + 2
    Selection      = class_id + 3

    class Entry:
        def __init__(self, menu, id):
            self.menu = menu
            self.id   = id

        @property
        def tick(self):
            return swi.swi('Toolbox_ObjectMiscOp','0II;I',
                           self.menu.id, 1, self.id) != 0

        @tick.setter
        def tick(self, val):
            swi.swi('Toolbox_ObjectMiscOp','0IIII',
                    self.menu.id, 0, self.id, 1 if val else 0)

        @property
        def fade(self):
            return swi.swi('Toolbox_ObjectMiscOp','0II;I',
                           self.menu.id, 3, self.id,) != 0

        @fade.setter
        def fade(self, val):
            swi.swi('Toolbox_ObjectMiscOp','0IIII',
                    self.menu.id, 2, self.id, 1 if val else 0)

    def __init__(self, id):
        super().__init__(id)

    def __getitem__(self, item):
        return Menu.Entry(self, item)

    def event_handler(self, event_code, id_block, poll_block):
        if event_code == 0x828c3: # Menu_Selection
            return self.menu_selection(id_block)
        return False

    def menu_selection(self, item):
        return False