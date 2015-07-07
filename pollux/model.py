from collections import namedtuple


Datum = namedtuple('Datum', 'date, lname, value')


class SymptomStrength:

    UNKNOWN = -999
    NONE = 0
    LOW = 10
    MEDIUM = 20
    HIGH = 30
