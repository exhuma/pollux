import unittest

from pollux.emitter import Emitter, MemoryHandler


class TestEmitter(unittest.TestCase):

    def test_emit(self):
        emitter = Emitter()
        memory_handler = MemoryHandler()
        emitter.add_handler(memory_handler)
        emitter.emit('pollen_family_1', 10)
        emitter.emit('pollen_family_2', 10)
        emitter.emit('pollen_family_3', 10)
        result = memory_handler.emitted_values
        expected = {
            ('pollen_family_1', 10),
            ('pollen_family_2', 10),
            ('pollen_family_3', 10),
        }
        self.assertEqual(result, expected)
