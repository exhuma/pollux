'''
Reaction/Symptom thresholds. Based on P. G. von Wahl, 1999
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
    'corylus': class1,
    'alnus': class1,
    'betula': class1,
    'quercus': class1,
    'gramineae': class2,
    'plantago': class3,
    'rumex': class3,
    'chenopodium': class3,
    'artemisia': class4
}
