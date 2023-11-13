from ..base import get_object
from ..events import toolbox_handler

from ..objects.saveas import SaveAsSaveToFileEvent, SaveAsSaveCompletedEvent


class SaveAsMixin:
    @toolbox_handler(SaveAsSaveToFileEvent)
    def _save_to_file(self, event_code, id_block, event):
        saved = self.save_to_file(event.filename)
        if saved:
            saveas = get_object(id_block.self.id)
            saveas.file_save_completed(*saved)

    def save_to_file(self, filename):
        return None

    @toolbox_handler(SaveAsSaveCompletedEvent)
    def _save_completed(self, event_code, id_block, event):
        self.save_completed(event.filename)

    def save_completed(self, filename):
        pass
