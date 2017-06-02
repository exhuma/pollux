'''
Reaction/Symptom thresholds. Based on P. G. von Wahl, 1999

This module contains static data used in pollux.
'''
from collections import namedtuple


Threshold = namedtuple('Threshold', 'light, medium')
'''
Contains the two upper limits for "light" and "medium" symptoms. Everything
causes has strong symptoms.
'''

class1 = Threshold(10, 50)
class2 = Threshold(5, 30)
class3 = Threshold(3, 15)
class4 = Threshold(2, 6)


THRESHOLDS = {
    'alnus': class1,
    'betula': class1,
    'corylus': class1,
    'fraxinus': class1,
    'quercus': class1,
    'gramineae': class2,
    'chenopodium': class3,
    'plantago': class3,
    'rumex': class3,
    'artemisia': class4
}


GENERA = {
    'acer',
    'aesculus',
    'alnus',
    'ambrosia',
    'artemisia',
    'asteraceae',
    'betula',
    'carpinus',
    'castanea',
    'chenopodium',
    'corylus',
    'cupressaceae',
    'cyperaceae',
    'ericaceae',
    'fagus',
    'filipendula',
    'fraxinus',
    'gramineae',
    'juglans',
    'juncaceae',
    'larix',
    'pinaceae',
    'plantago',
    'platanus',
    'populus',
    'quercus',
    'rumex',
    'salix',
    'sambucus',
    'tilia',
    'ulmus',
    'umbellifereae',
    'urtica',
}
