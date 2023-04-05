from ..events import message_handler
from ..user_messages.data_transfer import *

import ctypes
import swi

class DataOpenMixin:
    @message_handler(DataOpenMessage)
    def _data_open(self, code, id_block, message):
        if self.data_open(message.path_name, message.file_type) != False:
            message.your_ref = message.my_ref
            message.action_code = Messages.DataLoadAck
            swi.swi("Wimp_SendMessage", "iIi",
                17, ctypes.addressof(message), message.sender)

    def data_open(self, filename, filetype):
        return False