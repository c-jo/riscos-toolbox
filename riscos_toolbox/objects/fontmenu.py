"""RISC OS Toolbox - FontDBox"""

from ..base import Object
import swi

class FontMenu(object):
    class_id = 0x82a40
    AboutToBeShown    = class_id + 0
    DialogueCompleted = class_id + 1
    Selection         = class_id + 2

    @property
    def font(self):
        return self._miscop_get_string(1)

    @font.setter
    def font(self, font):
        self._miscop_set_string(0, font)
