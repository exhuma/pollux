#!/usr/bin/env python
'''
Fetches a data-set for Luxembourg
'''
from argparse import ArgumentParser
from datetime import datetime, timedelta
from os.path import exists
import logging

from ecmwfapi import ECMWFDataServer

LOG = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('filename')
    return parser.parse_args()


def fetch(year, filename):
    if exists(filename):
        LOG.debug('Skipping existing file %r', filename)
        return

    current = datetime(year, 1, 1)
    end = datetime(year, 1, 31)
    step = timedelta(days=1)
    alldates = []
    while current <= end:
        alldates.append(current.strftime('%Y%d%m'))
        current += step

    args = {

        "class": "ep",
        "dataset": "cera20c",
        "date": "%s-01-01/to/%s-12-31" % (year, year),
        "expver": "1",
        "levtype": "sfc",
        "number": "0",
        "param": "89.228/139.128/164.128/167.128/170.128/174.128",
        "stream": "enda",
        "time": "12:00:00",
        "type": "an",
        "target": filename,
        # north/west/south/east
        "area": "50.5/5/49/7",
        "grid": "1.0/1.0"
    }

    server = ECMWFDataServer()
    server.retrieve(args)


def main():
    args = parse_args()
    fetch(2010, filename=args.filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
