from collections import namedtuple


Datum = namedtuple('Datum', 'date, lname, value')


class SymptomStrength:

    UNKNOWN = 'unknown'
    ERROR = 'error'
    NONE = 'none'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
