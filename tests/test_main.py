import unittest
from datetime import date
from os.path import dirname, join
from unittest.mock import MagicMock, call

from pkg_resources import resource_filename

from pollux.model import Datum

HERE = dirname(__file__)


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
