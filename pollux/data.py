'''
Reaction/Symptom thresholds. Based on P. G. von Wahl, 1999
'''
from collections import namedtuple


Threshold = namedtuple('Threshold', 'light, medium')
'''
Contains the two upper limits for "light" and "medium" symptoms. Everything
causes has strong symptoms.
'''

THRESHOLDS = {
    'hazel': Threshold(10, 50),
    'alder': Threshold(10, 50),
    'oak': Threshold(10, 50),
    'grass': Threshold(5, 30),
    'plantain': Threshold(3, 15),
    'sorrel': Threshold(3, 15),
    'fat hen': Threshold(3, 15),
    'mugwort': Threshold(2, 6)
}
