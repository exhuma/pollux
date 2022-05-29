import csv
import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, Generator
from urllib.parse import urlencode

from pollux import parse_html
from pollux.cache import Cache
from pollux.model import Datum

LOG = logging.getLogger(__name__)


def load_from_www(url: str) -> str:
    LOG.debug("Fetching from %r", url)
    import requests

    response = requests.get(url)
    return response.text


def fetch_from(
    start_date: date,
    end_date: date = datetime.now().date(),
    cache_folder: str = "",
) -> Generator[Datum, None, None]:
    """
    Return a generator over each value starting from start_date until end_date.
    """

    cache = None
    if cache_folder:
        cache = Cache(cache_folder)

    while start_date <= end_date:
        LOG.info(
            "Fetching data for %s (Week #%s)",
            start_date,
            start_date.strftime("%U"),
        )
        week_number = start_date.isocalendar()[1]
        url_args = [
            ("qsPage", "data"),
            ("year", start_date.year),
            ("week", week_number),
        ]
        query = urlencode(url_args)
        url = "http://www.pollen.lu/index.php?" + query
        if cache:
            html = cache.get(url)
        else:
            html = ""

        if not html:
            html = load_from_www(url)
            if cache and html:
                cache.put(url, html)

        if not html:
            LOG.error("Unable to get data from %r", url)
            continue

        data = parse_html(html)
        start_date = start_date + timedelta(weeks=1)
        for row in data:
            yield row


def to_csv(start: date, end: date, filename: str) -> None:
    """
    Scrape the pollen.lu site for data between two dates and write it into a CSV
    file.
    """
    rows = sorted(
        fetch_from(start, end, cache_folder="cache"), key=lambda x: x.date
    )

    names = sorted({row.lname for row in rows})
    collection: Dict[date, Dict[str, Any]] = {}
    for datum in rows:
        daily = collection.setdefault(datum.date, {})
        daily[datum.lname] = datum.value

    # Add the header
    output_rows = [["date"] + names]

    # Add the data-rows
    for item_date, values in sorted(collection.items(), key=lambda x: x[0]):
        row = [str(item_date)]
        for name in names:
            row.append(values[name])
        output_rows.append(row)
    with open(filename, "w", encoding="utf8") as fptr:
        writer = csv.writer(fptr)
        writer.writerows(output_rows)
    LOG.info("Data written to %r", filename)
