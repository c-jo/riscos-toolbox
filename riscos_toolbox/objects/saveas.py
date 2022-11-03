from .. import Object
from .. import EventDecoder
from .. import get_object
from .. import ToolboxEvent

import swi

class SaveAs(Object):
    class_id = 0x82bc0

    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    SaveToFile        = class_id + 2
    FillBuffer        = class_id + 3
    SaveCompleted     = class_id + 4

    @EventDecoder(SaveToFile)
    def decode_save_to_file(poll_block):
        return (poll_block.nullstring(16),)

    @EventDecoder(FillBuffer)
    def decode_fill_buffer(poll_block):
        return (poll_block[4], poll_block[5], poll_block[6])

    @EventDecoder(SaveCompleted)
    def decode_save_completed(poll_block):
        return (poll_block[4], poll_block.nullstring(20))

    def __init__(self, id):
        super().__init__(id)

    @property
    def window_id(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0II;I', self.id, 0)

    @property
    def title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 2)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI',
                self.id, 2, buf, buf_size)
        return buf.nullstring()

    @title.setter
    def title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 1, title)

    @property
    def file_name(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 4)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI',
                self.id, 4, buf, buf_size)
        return buf.nullstring()

    @file_name.setter
    def file_name(self, file_name):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 3, file_name)

    @property
    def file_type(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0II;I', self.id, 6)

    @file_type.setter
    def file_type(self, file_type):
        swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.id, 5, file_type)

    @property
    def file_size(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0II;I', self.id, 8)

    @file_size.setter
    def file_size(self, file_size):
        swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.id, 7, file_size)

    def selection_available(self, available):
        swi.swi('Toolbox_ObjectMiscOp', '0III', self.id, 9, available)

    def set_data_addresss(self, address, size, sel_addr, sel_size):
        swi.swi('Toolbox_ObjectMiscOp', '0IIIIII', self.id, 10,
                address, size, sel_addr, sel_size)

    def buffer_filled(self, buffer, bytes_written):
        swi.swi('Toolbox_ObjectMiscOp', '0IIII', self.id, 11,
                buffer, bytes_written)

    def file_save_completed(self, filename, saved=True):
        swi.swi('Toolbox_ObjectMiscOp', 'IIIs',
                1 if saved else 0, self.id, 12, filename)

class SaveAsMixin(object):
    def __init__(self, id):
       super().__init__(id)

    @ToolboxEvent(SaveAs.SaveToFile)
    def _saveas_save_to_file(self, event_code, id_block, filename):
        saved = self.save_to_file(filename)
        if saved:
            saveas = get_object(id_block.self.id)
            saveas.file_save_completed(*saved)

    def save_to_file(self, filename):
        return None

    @ToolboxEvent(SaveAs.SaveCompleted)
    def _saveas_save_completed(self, event_code, id_block,
                               wimp_message, filename):
        self.save_completed(filename)

    def save_completed(self, filename):
        pass
