"""RISC OS Toolbox module"""

import swi

#from .objects import Object
#from .objects.window import Window
from collections import namedtuple
#from .objects import _objects

# Toolbox-wide variables
_objects = {}

class IDBlock:
    def __init__(self):
        self.block = swi.block(6)

    def __str__(self):
        return "IDBlock: Ancestor ID:{} Component:{}, Parent ID:{} Component {}, Self ID:{} Component {}".format(self.block[0], self.block[1], self.block[2], self.block[3], self.block[4], self.block[5])

    @property
    def ancestor(self):
        return namedtuple('ancestor', ('id', 'component')) \
            (self.block[0], self.block.tosigned(1))
    @property
    def parent(self):
        return namedtuple('parent', ('id', 'component')) \
            (self.block[2], self.block.tosigned(3))
    @property
    def self(self):
        return namedtuple('self', ('id', 'component')) \
            (self.block[4], self.block.tosigned(5))


def get_object(id):
    if id in _objects:
        return _objects[id]
    else:
        return None

def find_object(name):
    for id,obj in _objects.items():
        if obj.name == name:
           return obj
    return None

def create_object(template, klass=None):
    id = swi.swi('Toolbox_CreateObject', 'Is;I', 0, template)
    if klass:
        _objects[id] = klass(id)
    else:
        obj_class = swi.swi('Toolbox_GetObjectClass', '0I;I', id)
        _objects[id] = Object.create(obj_class, template, id)
    return _objects[id]

class Component:
   def __init__(self, id):
       self.id = id

class Object:
    class_id  = None
    name      = None
    _classes  = {} # (Class ID,Name) -> Class

    def __init__(self, id):
        self.id = id
        self.components = {}

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

    def show(self, menu_semantics=False, submenu_semantics=False,
                   type=0, parent=None):
        flags = 0
        if menu_semantics:
            flags |= 1
        if submenu_semantics:
            flags |= 2

        if parent:
            parent_obj, parent_comp = parent.id, parent.component
        else:
            parent_obj = parent_comp = 0

        swi.swi('Toolbox_ShowObject','III0II',
                flags,self.id,type,parent_obj, parent_comp)

    def hide(self):
        swi.swi('Toolbox_HideObject','0I',self.id)

    @property
    def parent(self):
        id, comp_id = swi.swi('Toolbox_GetParent', '0I;Ii', self.id)
        if id in _objects:
            obj = _objects[id]
        else:
            obj = Object(id)
        if comp_id == -1:
            comp = None
        else:
            if comp_id in obj.components:
                comp = obj.components[comp_id]
            else:
                comp = Component(comp_id)

        return namedtuple('parent', ('object', 'component'))(obj,comp)

    def event_handler(self, event_code, id_block, poll_block):
        pass

    def wimp_handler(self, reason, id_block, poll_block):
        pass


_quit     = False
#_objects  = {}
_id_block = IDBlock()
_message_handlers = {}

def initialise(appdir):
    msgtrans_block = swi.block(4)
    wimp_messages  = swi.block(1)
    toolbox_events = swi.block(1)
    wimp_messages [0] = 0
    toolbox_events[0] = 0

    swi.swi('MessageTrans_OpenFile', 'bsi', msgtrans_block,
                                     appdir+'.Messages', 0)

    wimp_ver,task_handle,sprite_area = \
        swi.swi('Toolbox_Initialise','0Ibbsbb;III',
                560, wimp_messages, toolbox_events,
               appdir, msgtrans_block, _id_block.block)

def quit():
     global _quit
     _quit = True

def run():
    poll_block = swi.block(64)
    global _quit

    while not _quit:
        reason,sender = swi.swi('Wimp_Poll','Ib;I.I', 0b1, poll_block)

        if reason == 0x200: # Toolbox Event
            size       = poll_block[0]
            reference  = poll_block[1]
            event_code = poll_block[2]
            flags      = poll_block[3]

            if event_code == 0x44ec1: # Object_AutoCreated
                name      = poll_block.nullstring(0x10,size)
                obj_class = swi.swi('Toolbox_GetObjectClass', '0I;I',
                                    _id_block.self.id)
                _objects[_id_block.self.id] = \
                     Object.create(obj_class, name, _id_block.self.id)
                continue

            object  = get_object(_id_block.self.id)
            comp_id = _id_block.self.component

            if object:
                if comp_id in object.components:
                    component = object.components[comp_id]
                    component.event_handler(event_code, _id_block, poll_block)
                else:
                    object.event_handler(event_code, _id_block, poll_block)

        if reason == 2: # Open Window
            if _id_block.self.id in _objects:
                object = _objects[_id_block.self.id]
                object.wimp_handler(reason, _id_block, poll_block)

        if reason ==17 or reason == 18: # Wimp Message
            message = poll_block[4]
            if message == 0:
                _quit = True
            else:
                if message in _message_handlers:
                    _message_handlers[message](poll_block)

