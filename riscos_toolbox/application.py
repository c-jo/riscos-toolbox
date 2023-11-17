from .events import EventHandler, registered_wimp_events
from ._consts import Wimp
from . import initialise, run


wimp_event_masks = {
    Wimp.Null: Wimp.Poll.NullMask,
    Wimp.RedrawWindow: Wimp.Poll.RedrawWindowRequestMask,
    Wimp.PointerLeavingWindow: Wimp.Poll.PointerLeavingWindowMask,
    Wimp.PointerEnteringWindow: Wimp.Poll.PointerEnteringWindowMask,
    Wimp.MouseClick: Wimp.Poll.MouseClickMask,
    Wimp.KeyPressed: Wimp.Poll.KeyPressedMask,
    Wimp.LoseCaret: Wimp.Poll.LoseCaretMask,
    Wimp.GainCartet: Wimp.Poll.GainCaretMask,
    Wimp.PollwordNonZero: Wimp.Poll.PollWordNonZeroMask,
}

_application = None


def _make_poll_flags(events):
    flags = 0
    for (event, mask) in wimp_event_masks.items():
        if event not in events:
            flags |= mask
    return flags


class Application(EventHandler):
    def __init__(self, appdir, poll_flags=None, throwback=True):
        super().__init__()
        self.throwback = throwback
        global _application
        if poll_flags is not None:
            self.poll_flags = poll_flags
        else:
            self.poll_flags = _make_poll_flags(registered_wimp_events)
        initialise(appdir)

    def set_poll_flag(self, flag):
        self.poll_flags = self.poll_flags | flag

    def clear_poll_flag(self, flag):
        self.poll_flags = self.poll_flags & ~flag

    def run(self):
        run(self)
