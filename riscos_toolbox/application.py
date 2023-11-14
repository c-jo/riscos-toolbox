from .events import EventHandler, registered_wimp_events
from consts import Wimp
from . import initialise, run

_application = None


def _make_poll_flags(events):
    flags = 0

    if Wimp.Null not in events:
        flags |= Wimp.Poll.NullMask
    if Wimp.RedrawWindow not in events:
        flags |= Wimp.Poll.RedrawWindowRequestMask
    if Wimp.PointerLeavingWindow not in events:
        flags |= Wimp.Poll.PointerLeavingWindowMask
    if Wimp.PointerEnteringWindow not in events:
        flags |= Wimp.Poll.PointerEnteringWindowMask
    if Wimp.MouseClick not in events:
        flags |= Wimp.Poll.MouseClickMask
    if Wimp.KeyPressed not in events:
        flags |= Wimp.Poll.KeyPressedMask
    if Wimp.LoseCaret not in events:
        flags |= Wimp.Poll.LoseCaretMask
    if Wimp.GainCartet not in events:
        flags |= Wimp.Poll.GainCaretMask
    if Wimp.PollwordNonZero not in events:
        flags |= Wimp.Poll.PollWordNonZeroMask

    return flags


class Application(EventHandler):
    def __init__(self, appdir):
        super().__init__()
        global _application
        _application = self
        self.poll_flags = _make_poll_flags(registered_wimp_events)
        initialise(appdir)

    def set_poll_flag(self, flag):
        self.poll_flags = self.poll_flags | flag

    def clear_poll_flag(self, flag):
        self.poll_flags = self.poll_flags & ~flag

    def run(self):
        run(self)
