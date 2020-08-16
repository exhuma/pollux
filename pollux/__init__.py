import logging
from datetime import date as makedate
from functools import lru_cache
from re import compile
from time import strptime
from typing import Any, Dict, Iterable, Set
from urllib.parse import urlencode

from bs4 import BeautifulSoup  # type: ignore

from .data import THRESHOLDS
from .model import Datum, SymptomStrength

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


def warnings(data: Iterable[Datum], date: makedate) -> Dict[str, SymptomStrength]:
    """
    Returns warning classifications for a given date.
    """
    output = {}
    for row in data:
        if row.date != date:
            continue

        key = row.lname.lower()
        threshold = THRESHOLDS.get(key)
        if threshold:
            if row.value >= threshold.medium:
                output[key] = SymptomStrength.HIGH
            elif row.value >= threshold.light:
                output[key] = SymptomStrength.MEDIUM
            elif row.value > 0:
                output[key] = SymptomStrength.LOW
            elif row.value == 0:
                LOG.debug("No warning needed for %r", row)
            else:
                # value < 0
                LOG.warning("Illegal value: %r", row)
                output[key] = SymptomStrength.ERROR
        else:
            LOG.debug("Key for row %r not found in thresholds!", row)
            output[key] = SymptomStrength.UNKNOWN

    LOG.debug("Determined %d warnings.", len(output))
    return output


@lru_cache(maxsize=20)
def fetch_week(year: int, week: int, httplib: Any) -> Set[Datum]:
    """
    Fetches values for one specific week.
    """
    LOG.debug("Fetching data for year %r, week %r from the web", year, week)
    url_params = [
        ("qsPage", "data"),
        ("year", year),
        ("week", week),
    ]
    query = urlencode(url_params)
    url = "http://www.pollen.lu/index.php?" + query
    response = httplib.get(url)
    data = parse_html(response.text)
    return data


class Probe:
    def __init__(self, httplib: Any, emitlib: Any) -> None:
        self.httplib = httplib
        self.emitlib = emitlib

    def execute(self, date: makedate) -> None:
        LOG.debug("Executing probe for %s", date)
        data = fetch_week(date.strftime("%Y"), date.strftime("%U"), self.httplib)

        filtered = {datum for datum in data if datum.date == date}

        self.emitlib.disseminate(date, filtered)
