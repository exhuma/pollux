import unittest
from datetime import date

from pollux.emitter import Emitter, MemoryHandler
from pollux.model import Datum


class TestEmitter(unittest.TestCase):
    def test_emit(self):
        emitter = Emitter()
        memory_handler = MemoryHandler()
        emitter.add_handler(memory_handler)
        emitter.warn("pollen_family_1", "low")
        emitter.warn("pollen_family_2", "low")
        emitter.warn("pollen_family_3", "low")
        result = memory_handler.emitted_values
        expected = {
            ("pollen_family_1", "low"),
            ("pollen_family_2", "low"),
            ("pollen_family_3", "low"),
        }
        self.assertEqual(result, expected)

    def test_disseminate(self):
        emitter = Emitter()
        memory_handler = MemoryHandler()
        emitter.add_handler(memory_handler)
        emitter.disseminate(
            date(2014, 4, 11),
            {
                Datum(date(2014, 4, 11), "Acer", 2),
                Datum(date(2014, 4, 11), "Aesculus", 0),
            },
        )
        result = memory_handler.disseminated_data
        expected = {
            "date": date(2014, 4, 11),
            "values": {
                Datum(date(2014, 4, 11), "Acer", 2),
                Datum(date(2014, 4, 11), "Aesculus", 0),
            },
        }
        self.assertEqual(result, expected)
