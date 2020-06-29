"""RISC OS Toolbox module"""

from swi import swi, block, integer

from .objects import Object, Window

class IDBlock:
    def __init__(self):
        self.block = block(6)

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

_quit     = False
_objects  = {}
_id_block = IDBlock()

def quit():
     global _quit
     _quit = True

def run():
    poll_block = block(64)

    while not _quit:
        reason,sender = swi('Wimp_Poll','0b;I.I', poll_block)

        if reason == 0x200: # Toolbox Event
            size       = poll_block[0]
            reference  = poll_block[1]
            event_code = poll_block[2]
            flags      = poll_block[3]

            if event_code == 0x44ec1: # Object_AutoCreate
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

        if reason == 17: # Wimp Message
            if poll_block[4] == 0:
                quit()
