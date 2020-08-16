from datetime import date
from enum import Enum
from typing import NamedTuple

Datum = NamedTuple(
    'Datum',
    [
        ('date', date),
        ('lname', str),
        ('value', int),
    ]
)


class SymptomStrength(str, Enum):

    UNKNOWN = 'unknown'
    ERROR = 'error'
    NONE = 'none'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
