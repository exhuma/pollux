from datetime import date
from typing import NamedTuple

Datum = NamedTuple("Datum", [("date", date), ("lname", str), ("value", int),])
