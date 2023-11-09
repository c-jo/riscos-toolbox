from .events import EventHandler
from consts import Wimp
from . import initialise, run

_application = None

class Application(EventHandler):
    def __init__(self, appdir):
        super().__init__()
        global _application
        _application = self
        self.poll_flags = Wimp.Poll.NullMask
        initialise(appdir)

    def set_poll_flag(self, flag):
        self.poll_flags = poll_flags | flag

    def clear_poll_flag(self, flag):
        self.poll_flags = poll_flags & ~flag

    def run(self):
        run(self)
