from ..events import WimpMessage
import ctypes
import swi

class Messages:
    DataOpen = 5

class DataOpenMixin:
    @WimpMessage(Messages.DataOpen)
    def data_open(self, message, id_block, poll_block):
        filetype = poll_block[10]
        filename = poll_block.nullstring(44)

        if self.on_data_open(filename, filetype) != False:
            poll_block[3] = poll_block[2]
            poll_block[4] = 4
            swi.swi("Wimp_SendMessage", "ibi", 17, poll_block, poll_block[1])

    def on_data_open(self, filename, filetype):
        return False