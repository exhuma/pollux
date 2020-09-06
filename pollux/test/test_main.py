from datetime import date
from pkg_resources import resource_filename
from unittest.mock import MagicMock, call
import unittest

from pollux import warnings
from pollux.model import Datum, SymptomStrength


class TestWarnings(unittest.TestCase):
    def setUp(self):
        self.data = {
            # untested date a
            Datum(date(2014, 4, 12), "gramineae", 100),
            Datum(date(2014, 4, 12), "quercus", 100),
            Datum(date(2014, 4, 12), "betula", 100),
            # tested date a
            Datum(date(2014, 4, 11), "betula", 80),
            Datum(date(2014, 4, 11), "gramineae", 3),
            Datum(date(2014, 4, 11), "quercus", 11),
            # untested date b
            Datum(date(2014, 4, 13), "gramineae", 200),
            Datum(date(2014, 4, 13), "quercus", 200),
            Datum(date(2014, 4, 13), "betula", 200),
            # tested date b
            Datum(date(2014, 4, 14), "betula", -10),
            Datum(date(2014, 4, 14), "gramineae", 0),
            Datum(date(2014, 4, 14), "quercus", 0),
            # tested date c
            Datum(date(2014, 4, 15), "betula", 0),
            Datum(date(2014, 4, 15), "gramineae", 0),
            Datum(date(2014, 4, 15), "quercus", 0),
        }

    def test_warnings(self):
        result = warnings(self.data, date(2014, 4, 11))
        expected = {
            "betula": SymptomStrength.HIGH,
            "gramineae": SymptomStrength.LOW,
            "quercus": SymptomStrength.MEDIUM,
        }
        self.assertEqual(result, expected)

    def test_warnings_error(self):
        result = warnings(self.data, date(2014, 4, 14))
        expected = {
            "betula": SymptomStrength.ERROR,
        }
        self.assertEqual(result, expected)

    def test_warnings_none(self):
        result = warnings(self.data, date(2014, 4, 15))
        expected = {}
        self.assertEqual(result, expected)

    def test_warnings_no_data(self):
        result = warnings(self.data, date(1100, 4, 11))
        expected = {}
        self.assertEqual(result, expected)


class TestMain(unittest.TestCase):
    def test_execute(self):
        from pollux import Probe

        fn = resource_filename("pollux", "test/data/data2.html")
        with open(fn, encoding="latin1") as fptr:
            html = fptr.read()

        http_get = MagicMock()
        http_get().return_value = MagicMock(text=html)
        httplib = MagicMock(get=http_get())
        emitlib = MagicMock()
        probe = Probe(httplib, emitlib)
        probe.execute(date(2014, 4, 11))
        httplib.get.assert_called_with(
            "http://www.pollen.lu/index.php?qsPage=data&year=2014&week=14"
        )
        emitlib.disseminate.assert_called_with(
            date(2014, 4, 11),
            {
                Datum(date(2014, 4, 11), "Acer", 2),
                Datum(date(2014, 4, 11), "Aesculus", 0),
                Datum(date(2014, 4, 11), "Alnus", 0),
                Datum(date(2014, 4, 11), "Ambrosia", 0),
                Datum(date(2014, 4, 11), "Artemisia", 0),
                Datum(date(2014, 4, 11), "Asteraceae", 0),
                Datum(date(2014, 4, 11), "Betula", 117),
                Datum(date(2014, 4, 11), "Carpinus", 5),
                Datum(date(2014, 4, 11), "Castanea", 0),
                Datum(date(2014, 4, 11), "Chenopodium", 0),
                Datum(date(2014, 4, 11), "Corylus", 0),
                Datum(date(2014, 4, 11), "Cupressaceae", 3),
                Datum(date(2014, 4, 11), "Cyperaceae", 1),
                Datum(date(2014, 4, 11), "Ericaceae", 0),
                Datum(date(2014, 4, 11), "Fagus", 112),
                Datum(date(2014, 4, 11), "Filipendula", 0),
                Datum(date(2014, 4, 11), "Fraxinus", 5),
                Datum(date(2014, 4, 11), "Gramineae", 1),
                Datum(date(2014, 4, 11), "Juglans", 1),
                Datum(date(2014, 4, 11), "Juncaceae", 0),
                Datum(date(2014, 4, 11), "Larix", 1),
                Datum(date(2014, 4, 11), "Pinaceae", 13),
                Datum(date(2014, 4, 11), "Plantago", 0),
                Datum(date(2014, 4, 11), "Platanus", 4),
                Datum(date(2014, 4, 11), "Populus", 0),
                Datum(date(2014, 4, 11), "Quercus", 15),
                Datum(date(2014, 4, 11), "Rumex", 0),
                Datum(date(2014, 4, 11), "Salix", 5),
                Datum(date(2014, 4, 11), "Sambucus", 0),
                Datum(date(2014, 4, 11), "Tilia", 0),
                Datum(date(2014, 4, 11), "Ulmus", 0),
                Datum(date(2014, 4, 11), "Umbellifereae", 0),
                Datum(date(2014, 4, 11), "Urtica", 0),
            },
        )

    def test_week_startday(self):
        """
        The week on pollen.lu starts on a Sunday. We need to make sure this is
        correctly called.
        """
        from pollux import Probe

        http_get = MagicMock()
        http_get().return_value = MagicMock(text="")
        httplib = MagicMock(get=http_get())
        emitlib = MagicMock()
        probe = Probe(httplib, emitlib)
        probe.execute(date(2015, 7, 5))
        httplib.get.assert_called_with(
            "http://www.pollen.lu/index.php?qsPage=data&year=2015&week=27"
        )
