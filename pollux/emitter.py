import logging

LOG = logging.getLogger(__name__)


class MemoryHandler:

    def __init__(self):
        self.emitted_values = set()

    def handle(self, pollen_family, symptom_strength):
        LOG.info('Memorizing %r, %r', pollen_family, symptom_strength)
        self.emitted_values.add((pollen_family, symptom_strength))

    def handle_raw_data(self, data):
        LOG.info('Memorizing %r', data)
        self.disseminated_data = data


class Emitter:

    def __init__(self):
            self.handlers = set()

    def add_handler(self, handler):
        self.handlers.add(handler)

    def warn(self, pollen_family, symptom_strength):
        for handler in self.handlers:
            handler.handle(pollen_family, symptom_strength)

    def disseminate(self, date, values):
        output = {
            'date': date,
            'values': values
        }
        for handler in self.handlers:
            handler.handle_raw_data(output)
