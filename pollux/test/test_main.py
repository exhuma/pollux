from datetime import date
from pkg_resources import resource_filename
from unittest.mock import MagicMock, call
import unittest

from pollux import warnings
from pollux.model import Datum, SymptomStrength


class TestWarnings(unittest.TestCase):

    def setUp(self):
        self.data = {
            # earlier date
            Datum(date(2014, 4, 12), 'gramineae', 100),
            Datum(date(2014, 4, 12), 'quercus', 100),
            Datum(date(2014, 4, 12), 'betula', 100),
            # tested date
            Datum(date(2014, 4, 11), 'gramineae', 3),
            Datum(date(2014, 4, 11), 'quercus', 11),
            Datum(date(2014, 4, 11), 'betula', 80),
            # later date
            Datum(date(2014, 4, 13), 'gramineae', 200),
            Datum(date(2014, 4, 13), 'quercus', 200),
            Datum(date(2014, 4, 13), 'betula', 200),
        }
        self.tested_date = date(2014, 4, 11)

    def test_warnings(self):
        result = warnings(self.data, self.tested_date)
        expected = {
            'betula': SymptomStrength.HIGH,
            'quercus': SymptomStrength.MEDIUM,
            'gramineae': SymptomStrength.LOW,
        }
        self.assertEqual(result, expected)

    def test_warnings_no_data(self):
        result = warnings(self.data, date(1100, 4, 11))
        expected = {}
        self.assertEqual(result, expected)


class TestMain(unittest.TestCase):

    def test_execute(self):
        from pollux import Probe

        fn = resource_filename('pollux', 'test/data/data2.html')
        with open(fn, encoding='latin1') as fptr:
            html = fptr.read()

        http_get = MagicMock()
        http_get().return_value = MagicMock(text=html)
        httplib = MagicMock(get=http_get())
        emitlib = MagicMock()
        probe = Probe(httplib, emitlib)
        probe.execute(date(2014, 4, 11))
        httplib.get.assert_called_with(
            'http://www.pollen.lu/index.php?qsPage=data&year=2014&week=14')
        emitlib.emit.assert_has_calls([
            call('gramineae', 10),
            call('betula', 30),
            call('quercus', 20),
        ], any_order=True)

    def test_week_startday(self):
        '''
        The week on pollen.lu starts on a Sunday. We need to make sure this is
        correctly called.
        '''
        from pollux import Probe

        http_get = MagicMock()
        http_get().return_value = MagicMock(text='')
        httplib = MagicMock(get=http_get())
        emitlib = MagicMock()
        probe = Probe(httplib, emitlib)
        probe.execute(date(2015, 7, 5))
        httplib.get.assert_called_with(
            'http://www.pollen.lu/index.php?qsPage=data&year=2015&week=27')
