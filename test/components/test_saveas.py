import unittest

import riscos_toolbox as toolbox
import riscos_toolbox.objects.saveas
import swi

TEST_OBJECT_ID = 0x1001
TEST_WINDOW_ID = 0x2001

_swi_responses = {
    ('Toolbox_ObjectMiscOp', '0II;I', TEST_OBJECT_ID, 0) : TEST_WINDOW_ID
}

def _testswi(*args):
    if args not in _swi_responses.keys():
        raise RuntimeError("Unexpcted SWI called")
    else:
        return _swi_responses[args]

swi.swi = _testswi

class SaveAs(unittest.TestCase):

    def test_window_id(self):
        saveas = riscos_toolbox.objects.saveas.SaveAs(TEST_OBJECT_ID)
        self.assertEqual(saveas.window_id, TEST_WINDOW_ID)

