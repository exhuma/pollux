import unittest
from datetime import date
from os.path import dirname, join

from pkg_resources import resource_filename

from pollux import Datum, parse_html

HERE = dirname(__file__)


class TestParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_parsing(self):
        fn = join(HERE, "data", "data1.html")
        with open(fn, encoding="latin1") as fptr:
            html = fptr.read()
        result = parse_html(html)
        expected = {
            Datum(date(2014, 9, 21), "Ambrosia", 0),
            Datum(date(2014, 9, 22), "Ambrosia", 1),
            Datum(date(2014, 9, 23), "Ambrosia", 0),
            Datum(date(2014, 9, 24), "Ambrosia", 0),
            Datum(date(2014, 9, 25), "Ambrosia", 0),
            Datum(date(2014, 9, 26), "Ambrosia", 0),
            Datum(date(2014, 9, 27), "Ambrosia", 0),
            Datum(date(2014, 9, 21), "Artemisia", 0),
            Datum(date(2014, 9, 22), "Artemisia", 0),
            Datum(date(2014, 9, 23), "Artemisia", 0),
            Datum(date(2014, 9, 24), "Artemisia", 0),
            Datum(date(2014, 9, 25), "Artemisia", 0),
            Datum(date(2014, 9, 26), "Artemisia", 0),
            Datum(date(2014, 9, 27), "Artemisia", 0),
            Datum(date(2014, 9, 21), "Asteraceae", 0),
            Datum(date(2014, 9, 22), "Asteraceae", 0),
            Datum(date(2014, 9, 23), "Asteraceae", 0),
            Datum(date(2014, 9, 24), "Asteraceae", 0),
            Datum(date(2014, 9, 25), "Asteraceae", 0),
            Datum(date(2014, 9, 26), "Asteraceae", 0),
            Datum(date(2014, 9, 27), "Asteraceae", 0),
            Datum(date(2014, 9, 21), "Alnus", 0),
            Datum(date(2014, 9, 22), "Alnus", 0),
            Datum(date(2014, 9, 23), "Alnus", 0),
            Datum(date(2014, 9, 24), "Alnus", 0),
            Datum(date(2014, 9, 25), "Alnus", 0),
            Datum(date(2014, 9, 26), "Alnus", 0),
            Datum(date(2014, 9, 27), "Alnus", 0),
            Datum(date(2014, 9, 21), "Betula", 0),
            Datum(date(2014, 9, 22), "Betula", 0),
            Datum(date(2014, 9, 23), "Betula", 0),
            Datum(date(2014, 9, 24), "Betula", 0),
            Datum(date(2014, 9, 25), "Betula", 0),
            Datum(date(2014, 9, 26), "Betula", 0),
            Datum(date(2014, 9, 27), "Betula", 0),
            Datum(date(2014, 9, 21), "Ericaceae", 0),
            Datum(date(2014, 9, 22), "Ericaceae", 0),
            Datum(date(2014, 9, 23), "Ericaceae", 0),
            Datum(date(2014, 9, 24), "Ericaceae", 0),
            Datum(date(2014, 9, 25), "Ericaceae", 0),
            Datum(date(2014, 9, 26), "Ericaceae", 0),
            Datum(date(2014, 9, 27), "Ericaceae", 0),
            Datum(date(2014, 9, 21), "Carpinus", 0),
            Datum(date(2014, 9, 22), "Carpinus", 0),
            Datum(date(2014, 9, 23), "Carpinus", 0),
            Datum(date(2014, 9, 24), "Carpinus", 0),
            Datum(date(2014, 9, 25), "Carpinus", 0),
            Datum(date(2014, 9, 26), "Carpinus", 0),
            Datum(date(2014, 9, 27), "Carpinus", 0),
            Datum(date(2014, 9, 21), "Castanea", 0),
            Datum(date(2014, 9, 22), "Castanea", 0),
            Datum(date(2014, 9, 23), "Castanea", 0),
            Datum(date(2014, 9, 24), "Castanea", 0),
            Datum(date(2014, 9, 25), "Castanea", 0),
            Datum(date(2014, 9, 26), "Castanea", 0),
            Datum(date(2014, 9, 27), "Castanea", 0),
            Datum(date(2014, 9, 21), "Quercus", 0),
            Datum(date(2014, 9, 22), "Quercus", 0),
            Datum(date(2014, 9, 23), "Quercus", 0),
            Datum(date(2014, 9, 24), "Quercus", 0),
            Datum(date(2014, 9, 25), "Quercus", 0),
            Datum(date(2014, 9, 26), "Quercus", 0),
            Datum(date(2014, 9, 27), "Quercus", 0),
            Datum(date(2014, 9, 21), "Chenopodium", 0),
            Datum(date(2014, 9, 22), "Chenopodium", 0),
            Datum(date(2014, 9, 23), "Chenopodium", 0),
            Datum(date(2014, 9, 24), "Chenopodium", 0),
            Datum(date(2014, 9, 25), "Chenopodium", 0),
            Datum(date(2014, 9, 26), "Chenopodium", 0),
            Datum(date(2014, 9, 27), "Chenopodium", 0),
            Datum(date(2014, 9, 21), "Cupressaceae", 0),
            Datum(date(2014, 9, 22), "Cupressaceae", 0),
            Datum(date(2014, 9, 23), "Cupressaceae", 0),
            Datum(date(2014, 9, 24), "Cupressaceae", 0),
            Datum(date(2014, 9, 25), "Cupressaceae", 0),
            Datum(date(2014, 9, 26), "Cupressaceae", 0),
            Datum(date(2014, 9, 27), "Cupressaceae", 0),
            Datum(date(2014, 9, 21), "Acer", 0),
            Datum(date(2014, 9, 22), "Acer", 0),
            Datum(date(2014, 9, 23), "Acer", 0),
            Datum(date(2014, 9, 24), "Acer", 0),
            Datum(date(2014, 9, 25), "Acer", 0),
            Datum(date(2014, 9, 26), "Acer", 0),
            Datum(date(2014, 9, 27), "Acer", 0),
            Datum(date(2014, 9, 21), "Fraxinus", 0),
            Datum(date(2014, 9, 22), "Fraxinus", 0),
            Datum(date(2014, 9, 23), "Fraxinus", 0),
            Datum(date(2014, 9, 24), "Fraxinus", 0),
            Datum(date(2014, 9, 25), "Fraxinus", 0),
            Datum(date(2014, 9, 26), "Fraxinus", 0),
            Datum(date(2014, 9, 27), "Fraxinus", 0),
            Datum(date(2014, 9, 21), "Gramineae", 0),
            Datum(date(2014, 9, 22), "Gramineae", 0),
            Datum(date(2014, 9, 23), "Gramineae", 0),
            Datum(date(2014, 9, 24), "Gramineae", 0),
            Datum(date(2014, 9, 25), "Gramineae", 2),
            Datum(date(2014, 9, 26), "Gramineae", 0),
            Datum(date(2014, 9, 27), "Gramineae", 0),
            Datum(date(2014, 9, 21), "Fagus", 0),
            Datum(date(2014, 9, 22), "Fagus", 0),
            Datum(date(2014, 9, 23), "Fagus", 0),
            Datum(date(2014, 9, 24), "Fagus", 0),
            Datum(date(2014, 9, 25), "Fagus", 0),
            Datum(date(2014, 9, 26), "Fagus", 0),
            Datum(date(2014, 9, 27), "Fagus", 0),
            Datum(date(2014, 9, 21), "Juncaceae", 0),
            Datum(date(2014, 9, 22), "Juncaceae", 0),
            Datum(date(2014, 9, 23), "Juncaceae", 0),
            Datum(date(2014, 9, 24), "Juncaceae", 0),
            Datum(date(2014, 9, 25), "Juncaceae", 0),
            Datum(date(2014, 9, 26), "Juncaceae", 0),
            Datum(date(2014, 9, 27), "Juncaceae", 0),
            Datum(date(2014, 9, 21), "Aesculus", 0),
            Datum(date(2014, 9, 22), "Aesculus", 0),
            Datum(date(2014, 9, 23), "Aesculus", 0),
            Datum(date(2014, 9, 24), "Aesculus", 0),
            Datum(date(2014, 9, 25), "Aesculus", 0),
            Datum(date(2014, 9, 26), "Aesculus", 0),
            Datum(date(2014, 9, 27), "Aesculus", 0),
            Datum(date(2014, 9, 21), "Larix", 0),
            Datum(date(2014, 9, 22), "Larix", 0),
            Datum(date(2014, 9, 23), "Larix", 0),
            Datum(date(2014, 9, 24), "Larix", 0),
            Datum(date(2014, 9, 25), "Larix", 0),
            Datum(date(2014, 9, 26), "Larix", 0),
            Datum(date(2014, 9, 27), "Larix", 0),
            Datum(date(2014, 9, 21), "Corylus", 0),
            Datum(date(2014, 9, 22), "Corylus", 0),
            Datum(date(2014, 9, 23), "Corylus", 0),
            Datum(date(2014, 9, 24), "Corylus", 0),
            Datum(date(2014, 9, 25), "Corylus", 0),
            Datum(date(2014, 9, 26), "Corylus", 0),
            Datum(date(2014, 9, 27), "Corylus", 0),
            Datum(date(2014, 9, 21), "Juglans", 0),
            Datum(date(2014, 9, 22), "Juglans", 0),
            Datum(date(2014, 9, 23), "Juglans", 0),
            Datum(date(2014, 9, 24), "Juglans", 0),
            Datum(date(2014, 9, 25), "Juglans", 0),
            Datum(date(2014, 9, 26), "Juglans", 0),
            Datum(date(2014, 9, 27), "Juglans", 0),
            Datum(date(2014, 9, 21), "Umbellifereae", 0),
            Datum(date(2014, 9, 22), "Umbellifereae", 0),
            Datum(date(2014, 9, 23), "Umbellifereae", 0),
            Datum(date(2014, 9, 24), "Umbellifereae", 0),
            Datum(date(2014, 9, 25), "Umbellifereae", 0),
            Datum(date(2014, 9, 26), "Umbellifereae", 0),
            Datum(date(2014, 9, 27), "Umbellifereae", 0),
            Datum(date(2014, 9, 21), "Ulmus", 0),
            Datum(date(2014, 9, 22), "Ulmus", 0),
            Datum(date(2014, 9, 23), "Ulmus", 0),
            Datum(date(2014, 9, 24), "Ulmus", 0),
            Datum(date(2014, 9, 25), "Ulmus", 0),
            Datum(date(2014, 9, 26), "Ulmus", 0),
            Datum(date(2014, 9, 27), "Ulmus", 0),
            Datum(date(2014, 9, 21), "Urtica", 2),
            Datum(date(2014, 9, 22), "Urtica", 1),
            Datum(date(2014, 9, 23), "Urtica", 3),
            Datum(date(2014, 9, 24), "Urtica", 1),
            Datum(date(2014, 9, 25), "Urtica", 3),
            Datum(date(2014, 9, 26), "Urtica", 2),
            Datum(date(2014, 9, 27), "Urtica", 4),
            Datum(date(2014, 9, 21), "Rumex", 0),
            Datum(date(2014, 9, 22), "Rumex", 0),
            Datum(date(2014, 9, 23), "Rumex", 0),
            Datum(date(2014, 9, 24), "Rumex", 0),
            Datum(date(2014, 9, 25), "Rumex", 0),
            Datum(date(2014, 9, 26), "Rumex", 0),
            Datum(date(2014, 9, 27), "Rumex", 0),
            Datum(date(2014, 9, 21), "Populus", 0),
            Datum(date(2014, 9, 22), "Populus", 0),
            Datum(date(2014, 9, 23), "Populus", 0),
            Datum(date(2014, 9, 24), "Populus", 0),
            Datum(date(2014, 9, 25), "Populus", 0),
            Datum(date(2014, 9, 26), "Populus", 0),
            Datum(date(2014, 9, 27), "Populus", 0),
            Datum(date(2014, 9, 21), "Pinaceae", 0),
            Datum(date(2014, 9, 22), "Pinaceae", 0),
            Datum(date(2014, 9, 23), "Pinaceae", 0),
            Datum(date(2014, 9, 24), "Pinaceae", 0),
            Datum(date(2014, 9, 25), "Pinaceae", 2),
            Datum(date(2014, 9, 26), "Pinaceae", 0),
            Datum(date(2014, 9, 27), "Pinaceae", 0),
            Datum(date(2014, 9, 21), "Plantago", 0),
            Datum(date(2014, 9, 22), "Plantago", 0),
            Datum(date(2014, 9, 23), "Plantago", 0),
            Datum(date(2014, 9, 24), "Plantago", 0),
            Datum(date(2014, 9, 25), "Plantago", 0),
            Datum(date(2014, 9, 26), "Plantago", 0),
            Datum(date(2014, 9, 27), "Plantago", 1),
            Datum(date(2014, 9, 21), "Platanus", 0),
            Datum(date(2014, 9, 22), "Platanus", 0),
            Datum(date(2014, 9, 23), "Platanus", 0),
            Datum(date(2014, 9, 24), "Platanus", 0),
            Datum(date(2014, 9, 25), "Platanus", 0),
            Datum(date(2014, 9, 26), "Platanus", 0),
            Datum(date(2014, 9, 27), "Platanus", 0),
            Datum(date(2014, 9, 21), "Salix", 0),
            Datum(date(2014, 9, 22), "Salix", 0),
            Datum(date(2014, 9, 23), "Salix", 0),
            Datum(date(2014, 9, 24), "Salix", 0),
            Datum(date(2014, 9, 25), "Salix", 0),
            Datum(date(2014, 9, 26), "Salix", 0),
            Datum(date(2014, 9, 27), "Salix", 0),
            Datum(date(2014, 9, 21), "Cyperaceae", 0),
            Datum(date(2014, 9, 22), "Cyperaceae", 0),
            Datum(date(2014, 9, 23), "Cyperaceae", 0),
            Datum(date(2014, 9, 24), "Cyperaceae", 0),
            Datum(date(2014, 9, 25), "Cyperaceae", 0),
            Datum(date(2014, 9, 26), "Cyperaceae", 0),
            Datum(date(2014, 9, 27), "Cyperaceae", 0),
            Datum(date(2014, 9, 21), "Filipendula", 0),
            Datum(date(2014, 9, 22), "Filipendula", 0),
            Datum(date(2014, 9, 23), "Filipendula", 0),
            Datum(date(2014, 9, 24), "Filipendula", 1),
            Datum(date(2014, 9, 25), "Filipendula", 1),
            Datum(date(2014, 9, 26), "Filipendula", 4),
            Datum(date(2014, 9, 27), "Filipendula", 2),
            Datum(date(2014, 9, 21), "Sambucus", 0),
            Datum(date(2014, 9, 22), "Sambucus", 0),
            Datum(date(2014, 9, 23), "Sambucus", 0),
            Datum(date(2014, 9, 24), "Sambucus", 0),
            Datum(date(2014, 9, 25), "Sambucus", 0),
            Datum(date(2014, 9, 26), "Sambucus", 0),
            Datum(date(2014, 9, 27), "Sambucus", 0),
            Datum(date(2014, 9, 21), "Tilia", 0),
            Datum(date(2014, 9, 22), "Tilia", 0),
            Datum(date(2014, 9, 23), "Tilia", 0),
            Datum(date(2014, 9, 24), "Tilia", 0),
            Datum(date(2014, 9, 25), "Tilia", 0),
            Datum(date(2014, 9, 26), "Tilia", 0),
            Datum(date(2014, 9, 27), "Tilia", 0),
        }
        self.assertCountEqual(result, expected)

    def test_parsing_2(self):
        fn = join(HERE, "data", "data2.html")
        with open(fn, encoding="latin1") as fptr:
            html = fptr.read()
        result = parse_html(html)

        expected = {
            Datum(date(2014, 4, 6), "Ambrosia", 0),
            Datum(date(2014, 4, 7), "Ambrosia", 0),
            Datum(date(2014, 4, 8), "Ambrosia", 0),
            Datum(date(2014, 4, 9), "Ambrosia", 0),
            Datum(date(2014, 4, 10), "Ambrosia", 0),
            Datum(date(2014, 4, 11), "Ambrosia", 0),
            Datum(date(2014, 4, 12), "Ambrosia", 0),
            Datum(date(2014, 4, 6), "Artemisia", 0),
            Datum(date(2014, 4, 7), "Artemisia", 0),
            Datum(date(2014, 4, 8), "Artemisia", 0),
            Datum(date(2014, 4, 9), "Artemisia", 0),
            Datum(date(2014, 4, 10), "Artemisia", 0),
            Datum(date(2014, 4, 11), "Artemisia", 0),
            Datum(date(2014, 4, 12), "Artemisia", 0),
            Datum(date(2014, 4, 6), "Asteraceae", 0),
            Datum(date(2014, 4, 7), "Asteraceae", 0),
            Datum(date(2014, 4, 8), "Asteraceae", 0),
            Datum(date(2014, 4, 9), "Asteraceae", 0),
            Datum(date(2014, 4, 10), "Asteraceae", 0),
            Datum(date(2014, 4, 11), "Asteraceae", 0),
            Datum(date(2014, 4, 12), "Asteraceae", 0),
            Datum(date(2014, 4, 6), "Alnus", 0),
            Datum(date(2014, 4, 7), "Alnus", 0),
            Datum(date(2014, 4, 8), "Alnus", 0),
            Datum(date(2014, 4, 9), "Alnus", 0),
            Datum(date(2014, 4, 10), "Alnus", 0),
            Datum(date(2014, 4, 11), "Alnus", 0),
            Datum(date(2014, 4, 12), "Alnus", 0),
            Datum(date(2014, 4, 6), "Betula", 166),
            Datum(date(2014, 4, 7), "Betula", 226),
            Datum(date(2014, 4, 8), "Betula", 229),
            Datum(date(2014, 4, 9), "Betula", 101),
            Datum(date(2014, 4, 10), "Betula", 37),
            Datum(date(2014, 4, 11), "Betula", 117),
            Datum(date(2014, 4, 12), "Betula", 69),
            Datum(date(2014, 4, 6), "Ericaceae", 0),
            Datum(date(2014, 4, 7), "Ericaceae", 0),
            Datum(date(2014, 4, 8), "Ericaceae", 0),
            Datum(date(2014, 4, 9), "Ericaceae", 0),
            Datum(date(2014, 4, 10), "Ericaceae", 0),
            Datum(date(2014, 4, 11), "Ericaceae", 0),
            Datum(date(2014, 4, 12), "Ericaceae", 0),
            Datum(date(2014, 4, 6), "Carpinus", 17),
            Datum(date(2014, 4, 7), "Carpinus", 12),
            Datum(date(2014, 4, 8), "Carpinus", 20),
            Datum(date(2014, 4, 9), "Carpinus", 4),
            Datum(date(2014, 4, 10), "Carpinus", 1),
            Datum(date(2014, 4, 11), "Carpinus", 5),
            Datum(date(2014, 4, 12), "Carpinus", 4),
            Datum(date(2014, 4, 6), "Castanea", 0),
            Datum(date(2014, 4, 7), "Castanea", 0),
            Datum(date(2014, 4, 8), "Castanea", 0),
            Datum(date(2014, 4, 9), "Castanea", 0),
            Datum(date(2014, 4, 10), "Castanea", 0),
            Datum(date(2014, 4, 11), "Castanea", 0),
            Datum(date(2014, 4, 12), "Castanea", 0),
            Datum(date(2014, 4, 6), "Quercus", 0),
            Datum(date(2014, 4, 7), "Quercus", 0),
            Datum(date(2014, 4, 8), "Quercus", 0),
            Datum(date(2014, 4, 9), "Quercus", 0),
            Datum(date(2014, 4, 10), "Quercus", 1),
            Datum(date(2014, 4, 11), "Quercus", 15),
            Datum(date(2014, 4, 12), "Quercus", 7),
            Datum(date(2014, 4, 6), "Chenopodium", 0),
            Datum(date(2014, 4, 7), "Chenopodium", 0),
            Datum(date(2014, 4, 8), "Chenopodium", 0),
            Datum(date(2014, 4, 9), "Chenopodium", 0),
            Datum(date(2014, 4, 10), "Chenopodium", 0),
            Datum(date(2014, 4, 11), "Chenopodium", 0),
            Datum(date(2014, 4, 12), "Chenopodium", 0),
            Datum(date(2014, 4, 6), "Cupressaceae", 8),
            Datum(date(2014, 4, 7), "Cupressaceae", 5),
            Datum(date(2014, 4, 8), "Cupressaceae", 5),
            Datum(date(2014, 4, 9), "Cupressaceae", 2),
            Datum(date(2014, 4, 10), "Cupressaceae", 2),
            Datum(date(2014, 4, 11), "Cupressaceae", 3),
            Datum(date(2014, 4, 12), "Cupressaceae", 0),
            Datum(date(2014, 4, 6), "Acer", 0),
            Datum(date(2014, 4, 7), "Acer", 0),
            Datum(date(2014, 4, 8), "Acer", 0),
            Datum(date(2014, 4, 9), "Acer", 1),
            Datum(date(2014, 4, 10), "Acer", 1),
            Datum(date(2014, 4, 11), "Acer", 2),
            Datum(date(2014, 4, 12), "Acer", 3),
            Datum(date(2014, 4, 6), "Fraxinus", 7),
            Datum(date(2014, 4, 7), "Fraxinus", 26),
            Datum(date(2014, 4, 8), "Fraxinus", 14),
            Datum(date(2014, 4, 9), "Fraxinus", 1),
            Datum(date(2014, 4, 10), "Fraxinus", 5),
            Datum(date(2014, 4, 11), "Fraxinus", 5),
            Datum(date(2014, 4, 12), "Fraxinus", 5),
            Datum(date(2014, 4, 6), "Gramineae", 0),
            Datum(date(2014, 4, 7), "Gramineae", 0),
            Datum(date(2014, 4, 8), "Gramineae", 0),
            Datum(date(2014, 4, 9), "Gramineae", 0),
            Datum(date(2014, 4, 10), "Gramineae", 1),
            Datum(date(2014, 4, 11), "Gramineae", 1),
            Datum(date(2014, 4, 12), "Gramineae", 0),
            Datum(date(2014, 4, 6), "Fagus", 2),
            Datum(date(2014, 4, 7), "Fagus", 25),
            Datum(date(2014, 4, 8), "Fagus", 15),
            Datum(date(2014, 4, 9), "Fagus", 13),
            Datum(date(2014, 4, 10), "Fagus", 56),
            Datum(date(2014, 4, 11), "Fagus", 112),
            Datum(date(2014, 4, 12), "Fagus", 75),
            Datum(date(2014, 4, 6), "Juncaceae", 0),
            Datum(date(2014, 4, 7), "Juncaceae", 0),
            Datum(date(2014, 4, 8), "Juncaceae", 0),
            Datum(date(2014, 4, 9), "Juncaceae", 0),
            Datum(date(2014, 4, 10), "Juncaceae", 0),
            Datum(date(2014, 4, 11), "Juncaceae", 0),
            Datum(date(2014, 4, 12), "Juncaceae", 0),
            Datum(date(2014, 4, 6), "Aesculus", 0),
            Datum(date(2014, 4, 7), "Aesculus", 0),
            Datum(date(2014, 4, 8), "Aesculus", 0),
            Datum(date(2014, 4, 9), "Aesculus", 0),
            Datum(date(2014, 4, 10), "Aesculus", 0),
            Datum(date(2014, 4, 11), "Aesculus", 0),
            Datum(date(2014, 4, 12), "Aesculus", 0),
            Datum(date(2014, 4, 6), "Larix", 0),
            Datum(date(2014, 4, 7), "Larix", 2),
            Datum(date(2014, 4, 8), "Larix", 2),
            Datum(date(2014, 4, 9), "Larix", 2),
            Datum(date(2014, 4, 10), "Larix", 0),
            Datum(date(2014, 4, 11), "Larix", 1),
            Datum(date(2014, 4, 12), "Larix", 0),
            Datum(date(2014, 4, 6), "Corylus", 0),
            Datum(date(2014, 4, 7), "Corylus", 0),
            Datum(date(2014, 4, 8), "Corylus", 0),
            Datum(date(2014, 4, 9), "Corylus", 0),
            Datum(date(2014, 4, 10), "Corylus", 0),
            Datum(date(2014, 4, 11), "Corylus", 0),
            Datum(date(2014, 4, 12), "Corylus", 0),
            Datum(date(2014, 4, 6), "Juglans", 0),
            Datum(date(2014, 4, 7), "Juglans", 0),
            Datum(date(2014, 4, 8), "Juglans", 0),
            Datum(date(2014, 4, 9), "Juglans", 0),
            Datum(date(2014, 4, 10), "Juglans", 0),
            Datum(date(2014, 4, 11), "Juglans", 1),
            Datum(date(2014, 4, 12), "Juglans", 0),
            Datum(date(2014, 4, 6), "Umbellifereae", 0),
            Datum(date(2014, 4, 7), "Umbellifereae", 0),
            Datum(date(2014, 4, 8), "Umbellifereae", 0),
            Datum(date(2014, 4, 9), "Umbellifereae", 0),
            Datum(date(2014, 4, 10), "Umbellifereae", 0),
            Datum(date(2014, 4, 11), "Umbellifereae", 0),
            Datum(date(2014, 4, 12), "Umbellifereae", 0),
            Datum(date(2014, 4, 6), "Ulmus", 0),
            Datum(date(2014, 4, 7), "Ulmus", 0),
            Datum(date(2014, 4, 8), "Ulmus", 3),
            Datum(date(2014, 4, 9), "Ulmus", 0),
            Datum(date(2014, 4, 10), "Ulmus", 0),
            Datum(date(2014, 4, 11), "Ulmus", 0),
            Datum(date(2014, 4, 12), "Ulmus", 0),
            Datum(date(2014, 4, 6), "Urtica", 0),
            Datum(date(2014, 4, 7), "Urtica", 0),
            Datum(date(2014, 4, 8), "Urtica", 0),
            Datum(date(2014, 4, 9), "Urtica", 0),
            Datum(date(2014, 4, 10), "Urtica", 0),
            Datum(date(2014, 4, 11), "Urtica", 0),
            Datum(date(2014, 4, 12), "Urtica", 0),
            Datum(date(2014, 4, 6), "Rumex", 0),
            Datum(date(2014, 4, 7), "Rumex", 0),
            Datum(date(2014, 4, 8), "Rumex", 0),
            Datum(date(2014, 4, 9), "Rumex", 0),
            Datum(date(2014, 4, 10), "Rumex", 0),
            Datum(date(2014, 4, 11), "Rumex", 0),
            Datum(date(2014, 4, 12), "Rumex", 0),
            Datum(date(2014, 4, 6), "Populus", 0),
            Datum(date(2014, 4, 7), "Populus", 0),
            Datum(date(2014, 4, 8), "Populus", 0),
            Datum(date(2014, 4, 9), "Populus", 0),
            Datum(date(2014, 4, 10), "Populus", 0),
            Datum(date(2014, 4, 11), "Populus", 0),
            Datum(date(2014, 4, 12), "Populus", 0),
            Datum(date(2014, 4, 6), "Pinaceae", 1),
            Datum(date(2014, 4, 7), "Pinaceae", 1),
            Datum(date(2014, 4, 8), "Pinaceae", 2),
            Datum(date(2014, 4, 9), "Pinaceae", 2),
            Datum(date(2014, 4, 10), "Pinaceae", 1),
            Datum(date(2014, 4, 11), "Pinaceae", 13),
            Datum(date(2014, 4, 12), "Pinaceae", 18),
            Datum(date(2014, 4, 6), "Plantago", 0),
            Datum(date(2014, 4, 7), "Plantago", 2),
            Datum(date(2014, 4, 8), "Plantago", 0),
            Datum(date(2014, 4, 9), "Plantago", 0),
            Datum(date(2014, 4, 10), "Plantago", 0),
            Datum(date(2014, 4, 11), "Plantago", 0),
            Datum(date(2014, 4, 12), "Plantago", 0),
            Datum(date(2014, 4, 6), "Platanus", 0),
            Datum(date(2014, 4, 7), "Platanus", 0),
            Datum(date(2014, 4, 8), "Platanus", 0),
            Datum(date(2014, 4, 9), "Platanus", 5),
            Datum(date(2014, 4, 10), "Platanus", 3),
            Datum(date(2014, 4, 11), "Platanus", 4),
            Datum(date(2014, 4, 12), "Platanus", 1),
            Datum(date(2014, 4, 6), "Salix", 2),
            Datum(date(2014, 4, 7), "Salix", 8),
            Datum(date(2014, 4, 8), "Salix", 11),
            Datum(date(2014, 4, 9), "Salix", 9),
            Datum(date(2014, 4, 10), "Salix", 4),
            Datum(date(2014, 4, 11), "Salix", 5),
            Datum(date(2014, 4, 12), "Salix", 0),
            Datum(date(2014, 4, 6), "Cyperaceae", 0),
            Datum(date(2014, 4, 7), "Cyperaceae", 0),
            Datum(date(2014, 4, 8), "Cyperaceae", 0),
            Datum(date(2014, 4, 9), "Cyperaceae", 0),
            Datum(date(2014, 4, 10), "Cyperaceae", 0),
            Datum(date(2014, 4, 11), "Cyperaceae", 1),
            Datum(date(2014, 4, 12), "Cyperaceae", 2),
            Datum(date(2014, 4, 6), "Filipendula", 0),
            Datum(date(2014, 4, 7), "Filipendula", 0),
            Datum(date(2014, 4, 8), "Filipendula", 0),
            Datum(date(2014, 4, 9), "Filipendula", 0),
            Datum(date(2014, 4, 10), "Filipendula", 0),
            Datum(date(2014, 4, 11), "Filipendula", 0),
            Datum(date(2014, 4, 12), "Filipendula", 0),
            Datum(date(2014, 4, 6), "Sambucus", 0),
            Datum(date(2014, 4, 7), "Sambucus", 0),
            Datum(date(2014, 4, 8), "Sambucus", 0),
            Datum(date(2014, 4, 9), "Sambucus", 0),
            Datum(date(2014, 4, 10), "Sambucus", 0),
            Datum(date(2014, 4, 11), "Sambucus", 0),
            Datum(date(2014, 4, 12), "Sambucus", 0),
            Datum(date(2014, 4, 6), "Tilia", 0),
            Datum(date(2014, 4, 7), "Tilia", 0),
            Datum(date(2014, 4, 8), "Tilia", 0),
            Datum(date(2014, 4, 9), "Tilia", 0),
            Datum(date(2014, 4, 10), "Tilia", 0),
            Datum(date(2014, 4, 11), "Tilia", 0),
            Datum(date(2014, 4, 12), "Tilia", 0),
        }
        self.assertCountEqual(result, expected)