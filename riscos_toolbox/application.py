from .events import EventHandler

_application = None

class Application(EventHandler):
    def __init__(self, appdir):
        super().__init__()
        global _application
        _application = self
        #toolbox.init(appdir)
