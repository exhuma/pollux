import logging
from datetime import date as makedate
from functools import lru_cache
from re import compile
from time import strptime
from typing import Any, Dict, Iterable, Set
from urllib.parse import urlencode

from bs4 import BeautifulSoup  # type: ignore
from .model import Datum

LOG = logging.getLogger(__name__)


def parse_html(data: str) -> Set[Datum]:
    """
    Parses HTML output from pollen.lu and returns structured data (a set of
    ``Datum`` instances).
    """
    output = set()  # type: Set[Datum]
    if not data:
        return output
    soup = BeautifulSoup(data, "html.parser")
    tables = soup.find_all("table")
    rows = tables[5].find_all("tr")
    dates_row = rows[1]
    data_rows = rows[2:]
    dates = [
        makedate(*strptime(cell.text, "%Y-%m-%d")[0:3])
        for cell in dates_row.find_all("td")[4:]
    ]
    for row in data_rows:
        cells = row.find_all("td")
        lname = cells[1].text
        values = [int(cell.text) for cell in cells[4:]]
        for date, value in zip(dates, values):
            output.add(Datum(date, lname, value))
    LOG.debug("Retrieved %d data", len(output))
    return output
