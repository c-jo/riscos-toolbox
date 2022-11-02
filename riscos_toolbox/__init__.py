"""RISC OS Toolbox module"""

import swi

from .types import BBox, Point
#from .objects import Object
#from .objects.window import Window
from collections import namedtuple
#from .objects import _objects

# Toolbox-wide variables
_objects = {} # ID -> Object

class IDBlock:
    def __init__(self):
        self.block = swi.block(6)

    def __str__(self):
        return "IDBlock: Ancestor ID:{:x} Component:{:x}, Parent ID:{:x} Component {:x}, Self ID:{:x} Component {:x}".format(self.block[0], self.block[1], self.block[2], self.block[3], self.block[4], self.block[5])

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
    messages  = {} # Message -> Handler fn
    _classes  = {} # (Class ID,Name) -> Class
    _messages = {} # (Message ID) -> [Class..]

    def __init__(self, id):
        self.id = id
        self.components = {}
        self._events = {} # (Event ID, Component/None) -> [Handlers]
        #print("Object.__init__", self, id)
        #print("_event_handlers", _event_handlers)
        for klass in self.__class__.mro():
            if klass == Object:
                break
            for event,handlers in _event_handlers.items():
                if klass.__qualname__ in handlers:
                    handler = handlers[klass.__qualname__]
                    if (event,None) in self._events:
                        self._events[(event,None)].append(handler)
                    else:
                        self._events[(event,None)] = [handler]

    def __init_subclass__(subclass):
        Object._classes[(subclass.class_id, subclass.name)] = subclass
        for message in subclass.messages:
            if message not in Object._messages:
                Object._messages[message] = [subclass]
            else:
                Object._messages[message].append(subclass)

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
        if (event_code,None) in self._events:
            if event_code in _event_decoders:
                args = _event_decoders[event_code](poll_block)
            else:
                args = (poll_block,)
            handlers = self._events[(event_code,None)]
            for handler in handlers:
                if handler(self, event_code, id_block, *args) != False:
                    return True
        return False

    def wimp_handler(self, reason, id_block, poll_block):
        return False

    def message_handler(self, message, polL_block):
        return None

_quit     = False
_id_block = IDBlock()

_message_decoders = {} # Message -> decoder
_message_handlers = {} # Messagge -> [ (cls,func) ... ]

_event_decoders = {} # Event -> decoder
_event_handlers = {} # Event -> { (class qualname -> func) }

def _message_dispatch(message, poll_block):
    if message not in _message_handlers.keys():
        return
    for (cls,handler) in _message_handlers[message]:
        if cls:
            for obj in _objects.values():
                if obj.__class__.__qualname__ == cls:
                    handler(obj, message, poll_block)

        else:
            handlers(message, poll_block)

def WimpMessage(message):
    def decorator(handler):
        if '.' in handler.__qualname__:
            cls = handler.__qualname__.rsplit('.',1)[0]
        else:
            cls = None

        if message in _message_handlers.keys():
            _message_handlers[message].append((cls,handler))
        else:
            _message_handlers[message] = [(cls,handler)]
        return handler
    return decorator

def _event_dispatch(event, id_block, poll_block):
    if event in _event_decoders.keys():
        data = _event_decoders[event](poll_block)
    else:
        data = (poll_block,)

    #print("_event_dispatch",event,id_block)
    for obj in filter(lambda o:o is not None,
                      map(get_object,
                          [ id_block.self.id,
                            id_block.parent.id,
                            id_block.ancestor.id ]
                          )):
        if obj.event_handler(event, id_block, poll_block) != False:
            return

    return
    if event not in _event_handlers.keys():
        return

    handlers = _event_handlers[event]
    #print(handlers)
    obj_ids = [id_block.self.id, id_block.parent.id, id_block.ancestor.id]

    for obj_id in obj_ids:
        obj = get_object(obj_id)
        #print(obj_id, obj,obj.__class__.__qualname__ if obj else None)
        if obj and obj.__class__.__qualname__ in handlers:
            if handlers[obj.__class__.__qualname__](obj, id_block, *data) != False:
                return

def ToolboxEvent(event, component=None):
    def decorator(handler):
        if '.' in handler.__qualname__:
            cls = handler.__qualname__.rsplit('.',1)[0]
        else:
            cls = None

        if event in _event_handlers.keys():
            _event_handlers[event][cls] = handler
        else:
            _event_handlers[event] = {cls:handler}
        return handler
    return decorator

def EventDecoder(event):
    def decorator(handler):
        _event_decoders[event] = handler
        return handler
    return decorator

def initialise(appdir):
    msgtrans_block = swi.block(4)
    messages = list(_message_handlers.keys()) + [0]
    wimp_messages = swi.block(len(messages))
    for index,message in zip(range(0,len(messages)),messages):
        wimp_messages[index] = message

    toolbox_events = swi.block(1)
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

            print("Toolbox event {:x}".format(event_code))
            if event_code == 0x44ec1: # Object_AutoCreated
                name      = poll_block.nullstring(0x10,size)
                obj_class = swi.swi('Toolbox_GetObjectClass', '0I;I',
                                    _id_block.self.id)
                _objects[_id_block.self.id] = \
                     Object.create(obj_class, name, _id_block.self.id)
                continue

            if event_code == 0x44ec2: # Object_Deleted
                print("Object {} delted". _id_block.self.id)

            _event_dispatch(event_code, _id_block, poll_block)

            #object  = get_object(_id_block.self.id)
            #comp_id = _id_block.self.component

            #if object:
            #    if comp_id in object.components:
            #        component = object.components[comp_id]
            #        component.event_handler(event_code, _id_block, poll_block)
            #    else:
            #        object.event_handler(event_code, _id_block, poll_block)

        if reason == 1: # Redraw Window
            block = poll_block
            object = get_object(swi.swi("Window_WimpToToolbox", "0Ii;I",
                                poll_block[0], -1))

            more = swi.swi("Wimp_RedrawWindow", ".b;I", poll_block)
            while more:
                visible = BBox( block.tosigned(1), block.tosigned(2),
                                block.tosigned(3), block.tosigned(4) )
                scroll =  Point( block.tosigned(5), block.tosigned(6) )
                redraw =  BBox( block.tosigned(7), block.tosigned(8),
                                block.tosigned(9), block.tosigned(10) )

                offset = Point( visible.min.x - scroll.x,
                                visible.max.y - scroll.y )
                if object:
                    object.on_redraw( visible, scroll, redraw, offset )

                more = swi.swi("Wimp_GetRectangle", ".b;I", poll_block)

        if reason == 2: # Open Window
            if _id_block.self.id in _objects:
                object = _objects[_id_block.self.id]
                object.wimp_handler(reason, _id_block, poll_block)

        if reason == 17 or reason == 18: # Wimp Message
            message = poll_block[4]
            if message == 0:
                _quit = True
            else:
                _message_dispatch(message, poll_block)

