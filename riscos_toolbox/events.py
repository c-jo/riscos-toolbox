"""RISC OS Toolbox library: events"""

from collections.abc import Iterable

from .base import Object, get_object

# Handlers
# --------
# The following is based on the toolbox event handlers. A similar mechanism
# is used for both wimp messages and wimp events.
# To handle a toolbox event, the @ToolboxEvent decorator is used on either a
# global function, or a member of a class which is derived from riscos_toolbox.
# Object or .Applicaton.
#
# When a toolbox event is recieved, the library will try each of the self,
# parent and ancestor objects, followed by the application object and then
# global functions for a handler. If one is found and it DOESN'T
# return False, the process with end. If the handler is not found, or returns
# False, the next one will be tried. Not returning anything from the handler
# will therefore cause further handlers not to be tried.

# Decoders
# --------
# Decoders are used to unpack the wimp's poll block into arguments for the
# handler function. They are optional - if a decoder is not provided the poll
# block is passed to the handler as-is.

# The dicts
# decoders : { event : decoder-func }
# handlers : { event : { class-name | None
#                            : { component | None : handler-function } } }

_event_decoders   = {}
_event_handlers   = {}
_wimp_decoders    = {}
_wimp_handlers    = {}
_message_decoders = {}
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

def _decode(item, decoders, poll_block):
    if item in decoders.keys():
        return decoders[item](poll_block)
    else:
        return (poll_block,)

def _object_dispatch(obj, code, handlers, id_block, args):
    cls = obj.__class__.__qualname__

    for k in obj.__class__.mro():
        if k == object:
            break
        cls = k.__qualname__
        if cls in handlers:
            handler = _handler_for_comp(handlers[cls], id_block.self.component)
            if handler(obj, code, id_block, *args) != False:
                return True

    return False

def _handler_for_comp(handlers, component_id):
    if component_id in handlers:
        return handlers[component_id]
    elif None in handlers:
        return handlers[None]
    else:
        return None

def _dispatch(item, decoders, handlers, id_block, poll_block):
    if item not in handlers:
        return

    handlers = handlers[item]

    from .base import _objects
    args = _decode(item, decoders, poll_block)
    # Does an object have a handler for this event?
    for obj in filter(lambda o:o is not None, map(get_object,
                          [ id_block.self.id,
                            id_block.parent.id,
                            id_block.ancestor.id ] )):
        if _object_dispatch(obj, item, handlers, id_block, args) != False:
            return # Handled

    # Other handlers (free functions)
    if None in handlers:
        handler = _handler_for_comp(handlers[None], id_block.self.component)
        if handler:
            handler(item, id_block, *args)

def event_dispatch(event, id_block, poll_block):
    _dispatch(event, _event_decoders, _event_handlers,
                     id_block, poll_block)

def message_dispatch(message, id_block, poll_block):
    _dispatch(message, _message_decoders, _message_handlers,
                       id_block, poll_block)

def wimp_dispatch(reason, id_block, poll_block):
    _dispatch(reason, _event_decoders, _wimp_handlers,
                      id_block, poll_block)
