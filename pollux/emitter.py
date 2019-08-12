'''
Emitters are responsible to work with both warningins and raw pollen data.
Emitters can have one or more handlers which /do/ something with the data they
are given.
'''
from warnings import warn
import logging

LOG = logging.getLogger(__name__)


class MemoryHandler:
    """
    Simply keep the values in-memory
    """

    def __init__(self):
        self.emitted_values = set()

    def handle(self, pollen_family, symptom_strength):
        LOG.info('Memorizing %r, %r', pollen_family, symptom_strength)
        self.emitted_values.add((pollen_family, symptom_strength))

    def handle_raw_data(self, data):
        LOG.info('Memorizing raw data: %r', data)
        self.disseminated_data = data


class CSVHandler:
    """
    Write the raw data to disk as CSV values.

    warnings are ignored.
    """

    def __init__(self, root_folder=None):
        self.root_folder = root_folder or 'csv_data'

    def handle(self, pollen_family, symptom_strength):
        warn('Not yet implemented', NotImplemented)

    def handle_raw_data(self, data):
        print(data)  # XXX debug statement


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


class CSVEmitter:

    def __init__(self):
            self.handlers = set()

    def disseminate(self, date, values):
        print(date, len(values))  # XXX debug statement
        from pprint import pprint; pprint(date)  # XXX debug statement
        from pprint import pprint; pprint(values)  # XXX debug statement
