"""RISC OS Toolbox library"""

import swi
import ctypes
import traceback
import struct
import sys

from ._types import *
from ._const import *
from .base import Object, _objects, get_object, create_object, find_objects, _application
from .events import *

_quit           = False
_id_block       = IDBlock()
_msgtrans_block = swi.block(4)


def task_name():
    try:
        name_len = swi.swi('Toolbox_GetSysInfo', 'I0;..I', 0)
        name_block = swi.block((name_len + 3) // 4)
        swi.swi('Toolbox_GetSysInfo', "Ib", 0, name_block)
        return name_block.nullstring()
    except Exception:
        return "Python Application"


def report_exception(e):
    error_block = swi.block(64)
    error_block[0] = 0
    error_block.padstring(str(e).encode('latin-1')[:250], b'\0', 4)

    if swi.swi('Wimp_ReportError', 'bIs000;.I',
               error_block, 0b000100000011, task_name()) == 2:
        global _quit
        _quit = True


def initialise(appdir):
    def _handler_block(handlers, add=[]):
        ids = sorted(
            list(
                filter(
                    lambda k: k >= 0, handlers.keys()
                )
            ) + add) + [0]
        block = swi.block(len(ids))
        for index, id in enumerate(ids):
            block[index] = id
        return block

    wimp_messages  = _handler_block(events._message_handlers,
                         list(events._reply_messages))
    toolbox_events = _handler_block(events._toolbox_handlers,
                         [Toolbox.ObjectAutoCreated, Toolbox.ObjectDeleted])

    wimp_ver, task_handle, sprite_area = \
        swi.swi('Toolbox_Initialise', '0IbbsbI;III',
                560, wimp_messages, toolbox_events,
                appdir, _msgtrans_block, ctypes.addressof(_id_block))


def msgtrans_lookup(token, *args, bufsize=256):
    args = args[:4]
    buffer = swi.block((bufsize + 3) // 4)
    swi.swi('MessageTrans_Lookup', 'bsbi' + ('s' * len(args)),
            _msgtrans_block, token, buffer, bufsize, *args)
    return buffer.ctrlstring()


def run(application):
    poll_buffer = (ctypes.c_byte * 256)()
    global _quit

    while not _quit:
        mask = 0 if events.null_polls() else 0b1

        reason,sender = swi.swi(
            'Wimp_Poll','II;I.I',
            mask, ctypes.addressof(poll_buffer))

        try:
            poll_block = bytes(poll_buffer)
            if reason == Wimp.ToolboxEvent:
                size, reference, event_code, flags = \
                    struct.unpack("IIII", poll_block[0:16])

                if event_code == Toolbox.ObjectAutoCreated:
                    name =''.join([chr(c) for c in \
                        iter(lambda i=iter(poll_block[0x10:]): next(i), 0)])

                    obj_class = swi.swi('Toolbox_GetObjectClass', '0I;I',
                                        _id_block.self.id)

                    _objects[_id_block.self.id] = Object.create(
                        obj_class, name, _id_block.self.id)
                    continue

                if event_code == Toolbox.ObjectDeleted:
                    if _id_block.self.id in _objects:
                        del _objects[_id_block.self.id]
                    continue

                toolbox_dispatch(event_code, application, _id_block, poll_block)

            elif reason in [
                    Wimp.UserMessage,
                    Wimp.UserMessageRecorded,
                    Wimp.UserMessageAcknowledge
                ]:
                message = MessageInfo.create(
                    reason, *struct.unpack("IIIII", poll_block[0:20]))

                if message == Messages.Quit:
                    _quit = True
                    continue

                message_dispatch(message, application, _id_block, poll_block)
            else:
                if reason == Wimp.Null:
                    events.null_poll()
                wimp_dispatch(reason, application, _id_block, poll_block)

        except Exception as e:
            report_exception(e)
            print(traceback.format_exc())


def quit():
    global _quit
    _quit = True
