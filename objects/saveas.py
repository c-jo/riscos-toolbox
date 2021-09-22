from . import Object
import swi

class SaveAs(Object):
    class_id = 0x82bc0
    def __init__(self, id):
        super().__init__(id)

    def event_handler(self, event_code, id_block, poll_block):
        print("SaveAs event handler {}".format(event_code))

        if event_code == SaveAs.class_id + 0: # SaveAs_AboutToBeShown
            self.about_to_be_shown(id_block)
        if event_code == SaveAs.class_id + 1: # SaveAs_DialogueCompleted
            self.dialogue_completed(id_block)
        if event_code == SaveAs.class_id + 2: # SaveAs_SaveToFile
            self.save_to_file(id_block, poll_block.nullstring(16))
        if event_code == SaveAs.class_id + 3: # SaveAs_FillBuffer
            self.fill_buffer(id_block,
                             poll_block[4], poll_block[5], poll_block[6])
        if event_code == SaveAs.class_id + 4: # SaveAs_SaveCompleted
            self.save_completed(id_block,
                                poll_block[4], poll_block.nullstring(20))

    def about_to_be_shown(self, id_nlock):
        pass

    def dialogue_completed(self, id_block):
        pass

    def save_to_file(self, id_block, filename):
        pass

    def fill_buffer(self, id_nlock, size, address, no_bytes):
        pass

    def save_completed(self, id_block, wimp_message, filename):
        pass

    def get_window_id(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.id, 0)

    def set_title(self, title):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 1, title)

    def get_title(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 2)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI',
                self.id, 2, buf, buf_size)
        return buf.nullstring()

    def set_file_name(self, file_name):
        swi.swi('Toolbox_ObjectMiscOp', '0IIs;I', self.id, 3, file_name)

    def get_file_name(self):
        buf_size = swi.swi('Toolbox_ObjectMiscOp', '0II00;....I', self.id, 4)
        buf = swi.block((buf_size+3)/4)
        swi.swi('Toolbox_ObjectMiscOp', '0IIbI',
                self.id, 4, buf, buf_size)
        return buf.nullstring()

    def set_file_type(self, file_type):
        swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.id, 5, file_type)

    def get_file_type(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0II;I', self.id, 6)

    def set_file_size(self, file_size):
        swi.swi('Toolbox_ObjectMiscOp', '0III;I', self.id, 7, file_size)

    def get_file_size(self):
        return swi.swi('Toolbox_ObjectMiscOp', '0II;I', self.id, 8)

    def selection_available(self, available):
        swi.swi('Toolbox_ObjectMiscOp', '0III', self.id, 9, available)

    def set_data_addresss(self, address, size, sel_addr, sel_size):
        return swi.swi('Toolbox_ObjectMiscOp', '0IIIIII', self.id, 10,
                       address, size, sel_addr, sel_size)

    def buffer_filled(self, buffer, bytes_written):
        return swi.swi('Toolbox_ObjectMiscOp', '0IIII', self.id, 11,
                       buffer, bytes_written)

    def file_save_completed(self, filename, saved=True):
        return swi.swi('Toolbox_ObjectMiscOp', 'IIIs',
                       1 if saved else 0, self.id, 12, filename)
