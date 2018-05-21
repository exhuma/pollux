import csv
import logging
from argparse import ArgumentParser
from datetime import date

from .stream import fetch_from


LOG = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('year', type=int)
    parser.add_argument('outfile')
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    return parser.parse_args()


def fetch_csv():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    start = date(args.year, 1, 1)
    end = date(args.year, 12, 31)
    rows = sorted(fetch_from(start, end, cache_folder='cache'),
                  key=lambda x: x.date)

    names = sorted({row.lname for row in rows})
    collection = {}
    for row in rows:
        daily = collection.setdefault(row.date, {})
        daily[row.lname] = row.value

    # Add the header
    rows = [['date'] + names]

    # Add the data-rows
    for item_date, values in sorted(collection.items(), key=lambda x: x[0]):
        row = [item_date]
        for name in names:
            row.append(values[name])
        rows.append(row)
    with open(args.outfile, 'w') as fptr:
        writer = csv.writer(fptr)
        writer.writerows(rows)
    LOG.info('Data written to %r', args.outfile)
