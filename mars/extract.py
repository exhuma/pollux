#!/usr/bin/env python3
"""
Script to convert a GRIBS file into a simple 2D-Table.

For our usage, a simple 2D table is sufficient.


Params:
    http://apps.ecmwf.int/codes/grib/param-db
MARS Post-Processing:
    https://software.ecmwf.int/wiki/display/UDOC/Post-processing+keywords
pygrib docs:
    https://jswhit.github.io/pygrib/docs/
"""

import logging
import pygrib
from argparse import ArgumentParser
from collections import namedtuple

Measurement = namedtuple('Measurement', 'name date value')

LOG = logging.getLogger(__name__)


def inspect(grib):
    '''
    Print out the available variable names and the used unit.
    '''
    names = {}
    for msg in grib:
        units = names.setdefault(msg.parameterName, set())
        units.add(msg.parameterUnits)

    for name, units in sorted(names.items(), key=lambda x: x[0]):
        print(name, sorted(units))


def tablify(grib, names):
    '''
    Return a table-like structure using timestamp as index (first column) and
    the variable name from *names* as subsequent columns.
    '''
    cols = {}
    for var in names:
        LOG.debug('Processing variable %r', var)
        iterator = iter(grib.select(name=var))
        for row in iterator:
            msr = Measurement(var, row.analDate, row.average)
            col = cols.setdefault(var, [])
            col.append(msr)

    for row in zip(*cols.values()):
        rowdata = {col.name: col for col in row}
        line = [row[0].date]
        for name in names:
            line.append(rowdata[name].value)
        yield line


def list_names(filename):
    print('Listing names in %r...' % filename)
    pygrib.tolerate_badgrib_on()
    grbs = pygrib.open(filename)
    inspect(grbs)
    grbs.close()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('outfile')
    parser.add_argument('-l', '--list-names',
                        default=False, action='store_true')
    parser.add_argument('-n', '--names')
    return parser.parse_args()


def convert(filename, cols):
    pygrib.tolerate_badgrib_on()
    grbs = pygrib.open(filename)
    # We need to consume the generator before closing the file
    output = list(tablify(grbs, cols))
    grbs.close()
    return output


def to_csv(filename, header, rows):
    import csv
    with open(filename, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    args = parse_args()
    if args.list_names:
        list_names(args.filename)
    else:
        names = [name.strip() for name in args.names.split(',')]
        rows = convert(args.filename, names)
        to_csv(args.outfile, names, rows)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
