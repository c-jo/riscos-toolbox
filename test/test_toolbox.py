import unittest
import sys
import fakeswi

sys.modules['swi'] = fakeswi

import riscos_toolbox as toolbox

class ToolboxTest(unittest.TestCase):
    def test_one(self):
        self.assertEqual(0,0)

