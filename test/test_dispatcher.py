import unittest
import sys

import riscos_toolbox as toolbox
from riscos_toolbox.events import toolbox_handler

id_block = toolbox.IDBlock()
id_block.self.id            = 0x1d001
id_block.self.component     = 0xc0001
id_block.parent.id          = 0x1d002
id_block.parent.component   = 0xc0002
id_block.ancestor.id        = 0x1d003
id_block.ancestor.component = 0xc0003

calls = []

class TestClass01(toolbox.Object):
    def __init__(self, id):
        super().__init__(id, "test")

    @toolbox_handler(0xc101)
    def event_c101(self, event, id_block, poll_block):
        calls.append((self.__class__.__name__, self.id, event, id_block, poll_block))

class TestClass02(toolbox.Object):
    def __init__(self, id):
        super().__init__(id, "test")

    @toolbox_handler(0xc102)
    def __init__(self, id):
        super().__init__(id)

    def event_c102(self, event, id_block, poll_block):
        calls.append((self.__class__.__name__, self.id, event, id_block, poll_block))

class TestClass03(toolbox.Object):
    def __init__(self, id):
        super().__init__(id, "test")

    @toolbox_handler(0xc103)
    def event_c103(self, event, id_block, poll_block):
        calls.append((self.__class__.__name__, self.id, event, id_block, poll_block))

@toolbox_handler(0xff01)
def test_func(event, id_block, *args):
    calls.append((test_func.__name__, None, event, id_block, args))

class ObjectDispatchTest(unittest.TestCase):
    def setUp(self):
        calls.clear()

    def test_self_handler(self):
        toolbox.base._objects[id_block.self.id] = TestClass01(id_block.self.id)
        toolbox.events.toolbox_dispatch(0xc101, None, id_block, None)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][2], 0xc101)

    def test_self_handler_different_call(self):
        toolbox.base._objects[id_block.self.id] = TestClass01(id_block.self.id)
        toolbox.events.toolbox_dispatch(0xa101, None, id_block, None)
        self.assertEqual(len(calls), 0)

    def test_parent_handler(self):
        toolbox.base._objects[id_block.parent.id] = TestClass01(id_block.parent.id)
        toolbox.events.toolbox_dispatch(0xc101, None, id_block, None)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][2], 0xc101)

    def test_ancesgtor_handler(self):
        toolbox.base._objects[id_block.ancestor.id] = TestClass01(id_block.ancestor.id)
        toolbox.events.toolbox_dispatch(0xc101, None, id_block, None)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][2], 0xc101)


class ObjectDispatchTestSame(unittest.TestCase):
    def setUp(self):
        calls.clear()
        toolbox.base._objects = {}

    def test_self_parent(self):
        toolbox.base._objects[id_block.self.id] = TestClass01(id_block.self.id)
        toolbox.base._objects[id_block.parent.id] = TestClass01(id_block.parent.id)
        toolbox.events.toolbox_dispatch(0xc101, None, id_block, None)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1], id_block.self.id)
        self.assertEqual(calls[0][2], 0xc101)

    def test_self_ancestor(self):
        toolbox.base._objects[id_block.self.id] = TestClass01(id_block.self.id)
        toolbox.base._objects[id_block.ancestor.id] = TestClass01(id_block.ancestor.id)
        toolbox.events.toolbox_dispatch(0xc101, None, id_block, None)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1], id_block.self.id)
        self.assertEqual(calls[0][2], 0xc101)

    def test_parent_ancestor(self):
        toolbox.base._objects[id_block.parent.id] = TestClass01(id_block.parent.id)
        toolbox.base._objects[id_block.ancestor.id] = TestClass01(id_block.ancestor.id)
        toolbox.events.toolbox_dispatch(0xc101, None, id_block, None)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1], id_block.parent.id)
        self.assertEqual(calls[0][2], 0xc101)
