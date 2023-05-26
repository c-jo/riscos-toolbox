import unittest

import fakeswi
import sys

sys.modules['swi'] = fakeswi

import riscos_toolbox as toolbox
import riscos_toolbox.objects.saveas

import swi

TEST_OBJECT_ID = 0x1001
TEST_WINDOW_ID = 0x2001
TEST_TITLE     = "Test Title"
TEST_NAME      = "Test"

class SwiMock:
    def __init__(self):
        self._expect = []
        self._pos = 0

    def swi(self, *args):
        if self._pos >= len(self._expect):
            raise RuntimeError("Unexpected SWI call")

        (exp,ret) = self._expect[self._pos]

        def argmatch(a,b):
            if len(a) != len(b):
                return False

            for i in range(len(a)):
                if a[i] != b[i] and a[i] is not None:
                    return False

            return True

        if not argmatch(exp,args):
            raise RuntimeError("SWI call mismatch: got {} exp {}".format(args, exp)) 

        self._pos += 1
        return ret

    def expect(self, exp, ret=None):
        data = (exp, ret)
        self._expect.append(data)

    @property
    def completed(self):
        return self._pos == len(self._expect)

class MockBlockString:
    def __init__(self, string):
        self.string = string

    def __call__(self, *args):
        return self

    def nullstring(self):
        return self.string

def expect_miscop(obj, op, ret):
    return (('Toolbox_ObjectMiscOp', 'III;I', 0, obj, op), ret)

def expect_miscop_string(swimock, obj, op, str):
    swimock.expect(('Toolbox_ObjectMiscOp', 'III00;....I', 0, obj, op), len(str))
    swimock.expect(('Toolbox_ObjectMiscOp', 'IIIbI', 0, obj, op, None, len(str)), None)

class SaveAs(unittest.TestCase):

    def test_window_id(self):
        swimock = SwiMock()
        swimock.expect(*expect_miscop(TEST_OBJECT_ID, 0, TEST_WINDOW_ID))
        swi.swi = swimock.swi

        saveas = riscos_toolbox.objects.saveas.SaveAs(TEST_OBJECT_ID, TEST_NAME)
        self.assertEqual(saveas.window_id, TEST_WINDOW_ID)
        self.assertTrue(swimock.completed)

    def test_get_title(self):
        swimock = SwiMock()

        expect_miscop_string(swimock, TEST_OBJECT_ID, 2, TEST_TITLE)
        swi.swi = swimock.swi
        swi.block = MockBlockString(TEST_TITLE)

        saveas = riscos_toolbox.objects.saveas.SaveAs(TEST_OBJECT_ID, TEST_NAME)
        self.assertEqual(saveas.title, "Test Title")
        self.assertTrue(swimock.completed)
