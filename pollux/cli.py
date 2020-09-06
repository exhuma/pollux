import csv
import logging
from argparse import ArgumentParser, Namespace
from datetime import date
from typing import Any, Dict

from .stream import fetch_from

LOG = logging.getLogger(__name__)


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("start_year", type=int)
    parser.add_argument("end_year", type=int)
    parser.add_argument("outfile")
    parser.add_argument("-v", "--verbose", default=False, action="store_true")
    return parser.parse_args()


def fetch_csv() -> None:
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    start = date(args.start_year, 1, 1)
    end = date(args.end_year, 12, 31)
    rows = sorted(fetch_from(start, end, cache_folder="cache"), key=lambda x: x.date)

    names = sorted({row.lname for row in rows})
    collection = {}  # type: Dict[date, Dict[str, Any]]
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
    with open(args.outfile, "w") as fptr:
        writer = csv.writer(fptr)
        writer.writerows(output_rows)
    LOG.info("Data written to %r", args.outfile)
