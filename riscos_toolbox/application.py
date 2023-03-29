from .events import EventHandler
from . import initialise, run

_application = None

class Application(EventHandler):
    def __init__(self, appdir):
        super().__init__()
        global _application
        _application = self
        initialise(appdir)

    def run(self):
        run(self)