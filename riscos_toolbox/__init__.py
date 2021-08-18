"""RISC OS Toolbox module"""

from swi import swi, block, integer

from .objects import Object, Window


class IDBlock:
    def __init__(self):
        self.block = block(6)

    def __str__(self):
        return "IDBlock: Ancestor ID:{:08x} Component:{:08x}, Parent ID:{:08x} Component {:08x}, Self ID:{:08x} Component {:08x}".format(self.block[0], self.block[1], self.block[2], self.block[3], self.block[4], self.block[5])

    @property
    def ancestor_id(self):
        return self.block[0]
    @property
    def ancestor_component(self):
        return self.block[1]
    @property
    def parent_id(self):
        return self.block[2]
    @property
    def parent_component(self):
        return self.block[3]
    @property
    def self_id(self):
        return self.block[4]
    @property
    def self_component(self):
        return self.block[5]

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

_quit     = False
_objects  = {}
_id_block = IDBlock()

def initialise(appdir):
    msgtrans_block = block(4)
    wimp_messages  = block(1)
    toolbox_events = block(1)
    wimp_messages [0] = 0
    toolbox_events[0] = 0

    swi('MessageTrans_OpenFile', 'bsi', msgtrans_block,
                                 appdir+'.Messages', 0)

    wimp_ver,task_handle,sprite_area = \
        swi('Toolbox_Initialise','0Ibbsbb;III',
            560, wimp_messages, toolbox_events,
            appdir, msgtrans_block, _id_block.block)

def quit():
     global _quit
     _quit = True

def run():
    poll_block = block(64)

    while not _quit:
        reason,sender = swi('Wimp_Poll','Ib;I.I', 0b1, poll_block)

        if reason == 0x200: # Toolbox Event
            size       = poll_block[0]
            reference  = poll_block[1]
            event_code = poll_block[2]
            flags      = poll_block[3]

            if event_code == 0x44ec1: # Object_AutoCreated
                name      = poll_block.nullstring(0x10,size)
                obj_class = swi('Toolbox_GetObjectClass', '0I;I',
                                _id_block.self_id)
                _objects[_id_block.self_id] = \
                     Object.create(obj_class, name, _id_block.self_id)
                continue

            object    = get_object(_id_block.self_id)
            component = _id_block.self_component

            if object:
                if isinstance(object,Window) and component in object.gadgets:
                    gadget = object.gadgets[component]
                    gadget.event_handler(event_code, _id_block, poll_block)
                else:
                    object.event_handler(event_code, _id_block, poll_block)

        if reason == 2: # Open Window
            if _id_block.self_id in _objects:
                object = _objects[_id_block.self_id]
                object.wimp_handler(reason, _id_block, poll_block)

        if reason == 17: # Wimp Message
            if poll_block[4] == 0:
                quit()
