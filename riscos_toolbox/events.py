"""RISC OS Toolbox library: events"""

from collections.abc import Iterable
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

# Decoders
# --------
# Decoders are used to unpack the wimp's poll block into arguments for the
# handler function. They are optional - if a decoder is not provided the poll
# block is passed to the handler as-is.

# The registry dicts
# decoders : { event : decoder-func }
# handlers : { event : { class-name
#                            : { component | None : handler-function } } }

class EventHandler(object):
    """Base class for things that can handle events."""
    def __init__(self):
        self.toolbox_handlers = {} # Event ID: Component ID: [Handlers]
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

            _build_handlers(_event_handlers,   self.toolbox_handlers, classname)
            _build_handlers(_wimp_handlers,    self.wimp_handlers,    classname)
            _build_handlers(_message_handlers, self.message_handlers, classname)

    def _dispatch(self, handlers, decoders, event, id_block, poll_block):
        if event not in handlers:
            return False

        handlers = handlers[event]
        component = id_block.self.component

        def _decode(event, decoders, poll_block):
            if event in decoders:
                return decoders[event](poll_block)
            else:
                return (poll_block,)

        if component in handlers:
            args = _decode(event, decoders, poll_block)
            for handler in handlers[component]:
                if handler(self, event, id_block, *args) != False:
                    return True

        if None in handlers:
            args = _decode(event, decoders, poll_block)
            for handler in handlers[None]:
                if handler(self, event, id_block, *args) != False:
                    return True

    def toolbox_dispatch(self, event, id_block, poll_block):
        return self._dispatch(self.toolbox_handlers, _event_decoders,
                              event, id_block, poll_block)

    def wimp_dispatch(self, event, id_block, poll_block):
        return self._dispatch(self.wimp_handlers, _wimp_decoders,
                              event, id_block, poll_block)

    def message_dispatch(self, event, id_block, poll_block):
        return self._dispatch(self.message_handlers, _message_decoders,
                              event, id_block, poll_block)

_event_decoders   = {}
_wimp_decoders    = {}
_message_decoders = {}

_event_handlers   = {}
_wimp_handlers    = {}
_message_handlers = {}

def _set_handler(code, component, handler, handlers):
    if '.' in handler.__qualname__:
        cls = handler.__qualname__.rsplit('.',1)[0]
    else:
        cls = None

    def _add_handler(handlers, code, component, cls, handler):
        handlers2 = {}
        if isinstance(code, Iterable):
            for component in component:
                handlers2[component] = handler
        else:
            handlers2[component] = handler

        if code in handlers.keys():
            handlers[code][cls] = handlers2
        else:
            handlers[code] = {cls:handlers2}

    if isinstance(code, Iterable):
        for code in code:
            _add_handler(handlers, code, component, cls, handler)
    else:
        _add_handler(handlers, code, component, cls, handler)

    return handler

def ToolboxEvent(event, component=None):
    def decorator(handler):
        return _set_handler(event, component, handler, _event_handlers)
    return decorator

def EventDecoder(event):
    def decorator(handler):
        _event_decoders[event] = handler
        return handler
    return decorator

def WimpMessage(message, component=None):
    def decorator(handler):
        return _set_handler(message, component, handler, _message_handlers)
    return decorator

def MessageDecoder(event):
    def decorator(handler):
        _message_decoders[event] = handler
        return handler
    return decorator

def WimpEvent(reason, component=None):
    def decorator(handler):
        return _set_handler(reason, component, handler, _wimp_handlers)
    return decorator

def WimpDecoder(event):
    def decorator(handler):
        _wimp_decoders[event] = handler
        return handler
    return decorator
