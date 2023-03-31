"""RISC OS Toolbox library: events"""

from collections.abc import Iterable
import ctypes
import inspect

# Handlers
# --------
# The following is based on the toolbox event handlers. A similar mechanism
# is used for both wimp messages and wimp events.
#
# To handle a toolbox event, the @ToolboxEvent decorator is used on a member of
# a class derived from riscos_toolbox.  event.EvebtDispatcher, such as .Object
# or .Application. The decorator can be used to match all components (with
# @ToolboxEvebt(event)...), one component (@ToolboxEvent(event, component)...)
# or a list of components (@ToolboxEvent(event, [comp1,comp2]...)
#
# When a toolbox event is recieved, the library will try each of the self,
# parent and ancestor objects, followed by the application object, to see if
# it has a suitable handler.
#
# For each level; if a a handler exists for the component id (from id_block.
# self.component) it will be called, or if no such handler exists, but there
# is an "all components" handler that will  be called.
#
# This means a "all components" handler from a more specific object will
# take precedence over a more specific one from a less specific object.
#
# If one is found and it DOESN'T return False, the process with end. If the
# handler is not found, or returns  False, the next one will be tried. Not
# returning anything from the handler will therefore cause further handlers not
# to be tried.

# handlers
# { event :
#     { class-name :
#         { component | None:
#             (handler-function, data-class | None )
#         }
#     }
# }

class EventData(object):
    event_id = None

    @classmethod
    def from_block(cls, data):
        """Create an object setup from `data` (a byte string). The default
           version here will setup a ctypes Structure derived class."""
        if issubclass(cls, ctypes.Structure):
            if len(data) < ctypes.sizeof(cls):
                raise RuntimeError("not enough data for "+cls.__name__)
            obj = cls()
            dst = ctypes.cast(
                ctypes.pointer(obj), ctypes.POINTER(ctypes.c_ubyte))
            for b in range(0, ctypes.sizeof(cls)):
                dst[b] = data[b]
            return obj

        else:
            raise RuntimeError("from_block not implemented for "+cls.__name__)

    @classmethod
    def from_poll_block(cls, poll_block):
        return cls.from_block(poll_block.tobytes())

    def __init__(self):
        super().__init__()

class EventHandler(object):
    """Base class for things that can handle events."""
    def __init__(self):
        self.toolbox_handlers = {} # event: component: [(handler, data-class)..]
        self.wimp_handlers    = {}
        self.message_handlers = {}

        def _build_handlers(registry, handlers, classname):
            for event, handler_map in registry.items():
                if classname in handler_map:
                    for component, handler in handler_map[classname].items():
                        if event not in handlers:
                            handlers[event] = {component:[handler]}
                        elif component not in handlers[event]:
                            handlers[event][component] = [handler]
                        else:
                            handlers[event][component].append(handler)

        for klass in inspect.getmro(self.__class__):
            classname = klass.__qualname__

            _build_handlers(_toolbox_handlers, self.toolbox_handlers, classname)
            _build_handlers(_wimp_handlers,    self.wimp_handlers,    classname)
            _build_handlers(_message_handlers, self.message_handlers, classname)

    def _dispatch(self, handlers, event, id_block, poll_block):
        if event not in handlers:
            return False

        handlers = handlers[event]
        component = id_block.self.component

        def _data(data_class, poll_block):
            if data_class is not None:
                return data_class.from_poll_block(poll_block)
            return poll_block

        if component in handlers:
            for handler,data_class in handlers[component]:
                if handler(self, event, id_block, _data(data_class, poll_block)) != False:
                    return True

        if None in handlers:
            for handler,data_class in handlers[None]:
                if handler(self, event, id_block, _data(data_class, poll_block)) != False:
                    return True

    def toolbox_dispatch(self, event, id_block, poll_block):
        return self._dispatch(self.toolbox_handlers,
                              event, id_block, poll_block)

    def wimp_dispatch(self, event, id_block, poll_block):
        return self._dispatch(self.wimp_handlers,
                              event, id_block, poll_block)

    def message_dispatch(self, event, id_block, poll_block):
        return self._dispatch(self.message_handlers,
                              event, id_block, poll_block)

_toolbox_handlers = {}
_wimp_handlers    = {}
_message_handlers = {}

def _set_handler(code, component, handler, handlers):
    if '.' in handler.__qualname__:
        cls = handler.__qualname__.rsplit('.',1)[0]
    else:
        cls = None

    def _add_handler(handlers, code, component, cls, handler):
        if isinstance(code, int):
            event_type = None
        elif issubclass(code, EventData):
            event_type = code
            code = code.event_id
        else:
            raise RuntimeError("Handler must be for int or EventData")

        if code in handlers.keys():
            if cls in handlers[code]:
                handlers[code][cls][component] = handler
            else:
                handlers[code][cls] = { component: (handler, event_tyoe) }
        else:
            handlers[code] = {cls:{ component: (handler, event_type) } }

    if isinstance(code, Iterable):
        for code in code:
            _add_handler(handlers, code, component, cls, handler)
    else:
        _add_handler(handlers, code, component, cls, handler)

    return handler

def ToolboxEvent(event, component=None):
    def decorator(handler):
        return _set_handler(event, component, handler, _toolbox_handlers)
    return decorator

def WimpMessage(message, component=None):
    def decorator(handler):
        return _set_handler(message, component, handler, _message_handlers)
    return decorator

def WimpEvent(reason, component=None):
    def decorator(handler):
        return _set_handler(reason, component, handler, _wimp_handlers)
    return decorator

# List of self, parent, ancestor, applcation with duplicated and None's removed.
# This is the list of objects to try to handle the event, in order.
def _get_spaa(application, id_block):
        from .base import get_object
        return list(
                filter(lambda o:o is not None,
                          map(get_object,
                              set( [id_block.self.id,
                                    id_block.parent.id,
                                    id_block.ancestor.id,
                                    application]
                                 )
                              )
                         )
               )

def toolbox_dispatch(event_code, application, id_block, poll_block):
    for obj in _get_spaa(application, id_block):
         if obj.toolbox_dispatch(event_code, id_block, poll_block):
             break

def message_dispatch(message, applicaton, id_block, poll_block):
    for obj in _get_spaa(application, id_block):
         if obj.message_dispatch(message, id_block, poll_block):
             break

def wimp_dispatch(reason, application, id_block, poll_block):
    for obj in _get_spaa(application, id_block):
         if obj.wimp_dispatch(reason, id_block, poll_block):
             break
