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

    def show(self, menu_semantics=False, submenu_semantics=False, type=0):
        swi.swi('Toolbox_ShowObject','III0II',0,self.id,type,0,0)

    def event_handler(self, event_code, id_block, poll_block):
        pass

    def wimp_handler(self, reason, id_block, poll_block):
        pass
