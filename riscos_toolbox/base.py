from collections import namedtuple
from .events import EventHandler

import swi

_objects = {}
_application = None


def get_object(id):
    if id in _objects:
        return _objects[id]
    else:
        return None


def find_objects(template):
    return [obj for obj in _objects.values() if obj.template == template]


def create_object(template, klass=None, args=None):
    id = swi.swi('Toolbox_CreateObject', 'Is;i', 0, template)
    if klass:
        if args is None:
            args = []
        _objects[id] = klass(id, template, *args)
    else:
        obj_class = swi.swi('Toolbox_GetObjectClass', 'Ii;i', 0, id)
        _objects[id] = Object.create(obj_class, template, id)
    return _objects[id]


def delete_object(object, recursive=True):
    if isinstance(object, Object):
        object = object.id # Take either an Object or its ID as an argument
        
    swi.swi('Toolbox_DeleteObject', 'Ii', 1 if recursive else 0, object)
    if object in _objects:
        del _objects[object]


class Component:
    def __init__(self, id):
        self.id = id


class Object(EventHandler):
    class_id = None
    template = None
    _classes = {}  # (Class ID,Template Name) -> Class

    def __init__(self, id, template):
        super().__init__()
        self.id = id
        self.template = template
        self.components = {}

    def __init_subclass__(subclass):
        Object._classes[(subclass.class_id, subclass.template)] = subclass

    @staticmethod
    def create(class_id, name, id):
        if (class_id, name) in Object._classes:
            return Object._classes[(class_id, name)](id, name)
        if (class_id, None) in Object._classes:
            return Object._classes[(class_id, None)](id, name)
        return Object(id, name)

    def show(self,
             menu_semantics=False, submenu_semantics=False,
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

        swi.swi('Toolbox_ShowObject', 'IiIIii',
                flags, self.id, type, 0, parent_obj, parent_comp)

    def hide(self):
        swi.swi('Toolbox_HideObject', 'Ii', 0, self.id)

    @property
    def parent(self):
        id, comp_id = swi.swi('Toolbox_GetParent', 'Ii;ii', 0, self.id)
        if id in _objects:
            obj = _objects[id]
        else:
            obj = Object(id, None)
        if comp_id == 0xffffffff:
            comp = None
        else:
            if comp_id in obj.components:
                comp = obj.components[comp_id]
            else:
                comp = Component(comp_id)

        return namedtuple('parent', ('object', 'component'))(obj, comp)

    def _miscop_get_signed(self, op):
        """Use Toolbox_ObjectMiscOp to get a signed integer."""
        return swi.swi("Toolbox_ObjectMiscOp", "IiI;i", 0, self.id, op)

    def _miscop_set_signed(self, op, value):
        """Use Toolbox_ObjectMiscOp to set a signed integer."""
        swi.swi("Toolbox_ObjectMiscOp", "IiIi", 0, self.id, op, value)

    def _miscop_get_unsigned(self, op):
        """Use Toolbox_ObjectMiscOp to get an unsigned integer."""
        return swi.swi("Toolbox_ObjectMiscOp", "IiI;I", 0, self.id, op)

    def _miscop_set_unsigned(self, op, value):
        """Use Toolbox_ObjectMiscOp to set an unsigned integer."""
        swi.swi("Toolbox_ObjectMiscOp", "IiII", 0, self.id, op, value)

    def _miscop_get_string(self, op):
        """Use Toolbox_ObjectMiscOp to get a string. This call will allocate
           a suitably-sized buffer, read the string and return it."""
        buf_size = swi.swi('Toolbox_ObjectMiscOp', 'IiI00;....i',
                           0, self.id, op)
        buf = swi.block((buf_size + 3) // 4)
        swi.swi('Toolbox_ObjectMiscOp', 'IiIbi', 0, self.id, op, buf, buf_size)
        return buf.nullstring()

    def _miscop_set_string(self, op, value):
        """Use Toolbox_ObjectMiscOp to set a string."""
        swi.swi("Toolbox_ObjectMiscOp", "IiIs", 0, self.id, op, value)
