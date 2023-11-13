from .events import EventHandler
from . import initialise, run

_application = None

class Application(EventHandler):
    def __init__(self, appdir, throwback=True):
        super().__init__()
        self.throwback = throwback
        global _application
        _application = self
        initialise(appdir)

    def run(self):
        run(self)