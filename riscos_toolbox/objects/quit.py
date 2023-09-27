"""RISC OS Toolbox - Quit"""

from ..base import Object
import swi

class Quit(Object):
    class_id = 0x82a90
    AboutToBeShown    = class_id + 0
    Quit              = class_id + 1
    DialogueCompleted = class_id + 2
    Cancel            = class_id + 3

    @property
    def window_id(self):
        return self._miscop_get_unsigned(0)

    @property
    def message(self):
        return self._miscop_get_string(2)

    @message.setter
    def message(self, message):
        self._miscop_set_string(1, message)

    @property
    def title(self):
        return self._miscop_get_string(4)

    @title.setter
    def title(self, title):
        self._miscop_set_string(3, title)
