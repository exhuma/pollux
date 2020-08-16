'''
Emitters are responsible to work with both warningins and raw pollen data.
Emitters can have one or more handlers which /do/ something with the data they
are given.
'''
import logging
from datetime import date
from typing import Any, Callable, Dict, Iterable, Set, Tuple

from pollux.model import Datum, SymptomStrength

LOG = logging.getLogger(__name__)


class MemoryHandler:
    """
    Simply keep the values in-memory
    """

    def __init__(self) -> None:
        self.emitted_values = set()  # type: Set[Tuple[str, SymptomStrength]]

    def handle(self, pollen_family: str, symptom_strength: SymptomStrength) -> None:
        LOG.info('Memorizing %r, %r', pollen_family, symptom_strength)
        self.emitted_values.add((pollen_family, symptom_strength))

    def handle_raw_data(self, data: Dict[str, Any]) -> None:
        LOG.info('Memorizing raw data: %r', data)
        self.disseminated_data = data


class Emitter:

    def __init__(self) -> None:
        self.handlers = set()  # type: Set[MemoryHandler]

    def add_handler(self, handler: MemoryHandler) -> None:
        self.handlers.add(handler)

    def warn(self, pollen_family: str, symptom_strength: SymptomStrength) -> None:
        for handler in self.handlers:
            handler.handle(pollen_family, symptom_strength)

    def disseminate(self, date: date, values: Iterable[Datum]) -> None:
        output = {
            'date': date,
            'values': values
        }
        for handler in self.handlers:
            handler.handle_raw_data(output)
