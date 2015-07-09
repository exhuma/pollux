import unittest

from pollux.emitter import Emitter, MemoryHandler


class TestEmitter(unittest.TestCase):

    def test_emit(self):
        emitter = Emitter()
        memory_handler = MemoryHandler()
        emitter.add_handler(memory_handler)
        emitter.emit('pollen_family_1', 'low')
        emitter.emit('pollen_family_2', 'low')
        emitter.emit('pollen_family_3', 'low')
        result = memory_handler.emitted_values
        expected = {
            ('pollen_family_1', 'low'),
            ('pollen_family_2', 'low'),
            ('pollen_family_3', 'low'),
        }
        self.assertEqual(result, expected)
