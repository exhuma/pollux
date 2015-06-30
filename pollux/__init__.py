from collections import namedtuple
from datetime import date as makedate
from re import compile
from time import strptime

from bs4 import BeautifulSoup

P_LNAME = compile(r'\((.*?)\)')

Datum = namedtuple('Datum', 'date, lname, value')


def parse(data):
    soup = BeautifulSoup(data, 'html.parser')
    tables = soup.find_all('table')
    rows = tables[5].find_all('tr')
    dates_row = rows[1]
    data = rows[2:]
    dates = [makedate(*strptime(cell.text, '%Y-%m-%d')[0:3])
             for cell in dates_row.find_all('td')[1:]]
    output = set()
    for row in data:
        cells = row.find_all('td')
        lname = P_LNAME.findall(cells[0].text)[0]
        values = [int(cell.text) for cell in cells[1:]]
        for date, value in zip(dates, values):
            output.add(Datum(date, lname, value))
    return output
