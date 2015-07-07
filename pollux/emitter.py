import logging

LOG = logging.getLogger(__name__)


class MemoryHandler:

    def __init__(self):
        self.emitted_values = set()

    def handle(self, pollen_family, symptom_strength):
        LOG.info('Memorizing %r, %r', pollen_family, symptom_strength)
        self.emitted_values.add((pollen_family, symptom_strength))


class Emitter:

    def __init__(self):
            self.handlers = set()

    def add_handler(self, handler):
        self.handlers.add(handler)

    def emit(self, pollen_family, symptom_strength):
        for handler in self.handlers:
            handler.handle(pollen_family, symptom_strength)
