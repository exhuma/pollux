"""
Command-line tools for pollux
"""
import logging
from argparse import ArgumentParser, Namespace
from datetime import date

from gouge.colourcli import Simple

from .stream import to_csv

LOG = logging.getLogger(__name__)


def parse_args() -> Namespace:
    """
    Parse comamnd-line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("start_year", type=int)
    parser.add_argument("end_year", type=int)
    parser.add_argument("outfile")
    parser.add_argument("-v", "--verbose", default=False, action="store_true")
    return parser.parse_args()


def fetch_csv() -> None:
    """
    Scrape the pollen.lu site for data and store it as CSV
    """
    args = parse_args()
    if args.verbose:
        Simple.basicConfig(level=logging.DEBUG, show_exc=True)
    else:
        Simple.basicConfig(level=logging.INFO, show_exc=True)

    start = date(args.start_year, 1, 1)
    end = date(args.end_year, 12, 31)
    to_csv(start, end, args.outfile)
