"""RISC OS Toolbox - Window"""

from .. import Object

class ProgInfo(Object):
    class_id = 0x82b40
    def __init__(self, id):
        super().__init__(id)
