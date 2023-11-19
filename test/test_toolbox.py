import unittest
import sys

import fakeswi

try:
    import swi
except ImportError:
    # Probably running on non-RISC OS system
    swi = sys.modules['swi']


class ToolboxTest(unittest.TestCase):
    def test_one(self):
        self.assertEqual(0, 0)
