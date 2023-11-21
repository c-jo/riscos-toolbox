import unittest
import sys

import test.fakeswi  # noqa
swi = sys.modules['swi']


class ToolboxTest(unittest.TestCase):
    def test_one(self):
        self.assertEqual(0, 0)
