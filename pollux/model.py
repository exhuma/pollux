from datetime import date
from typing import NamedTuple

from pydantic import BaseModel

Datum = NamedTuple(
    "Datum",
    [
        ("date", date),
        ("lname", str),
        ("value", int),
    ],
)


class Credentials(BaseModel):
    """
    User credentials used during the login process
    """

    username: str
    password: str
