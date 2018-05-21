import logging
from os import makedirs
from os.path import join, exists
from urllib.parse import urlencode, urlsplit, parse_qs

from datetime import datetime, timedelta

from pollux import parse_html


LOG = logging.getLogger(__name__)


class Cache:

    def __init__(self, root):
        self.root = root
        if not exists(root):
            LOG.info('Creating cache dir %r', root)
            makedirs(root)

    def _url_to_filename(self, url):
        url_parts = urlsplit(url)
        query_data = parse_qs(url_parts.query)
        year = query_data['year'][0]
        week = query_data['week'][0]
        return join(self.root, 'data-%s-%s.html' % (year, week))

    def get(self, url):
        LOG.debug('Fetching from cache: %r', url)
        filename = self._url_to_filename(url)
        if exists(filename):
            with open(filename, encoding='latin-1') as fp:
                data = fp.read()
        else:
            data = ''
        return data

    def put(self, url, data):
        LOG.debug('Storing to cache: %r', url)
        if not data:
            return
        filename = self._url_to_filename(url)
        if exists(filename):
            raise IOError('File %r exists!' % filename)
        with open(filename, 'w', encoding='latin-1') as fp:
            fp.write(data)


def load_from_www(url):
    LOG.debug('Fetching from %r', url)
    import requests
    response = requests.get(url)
    return response.text


def fetch_from(start_date, end_date=datetime.now().date(), cache_folder=''):
    '''
    Return a generator over each value starting from start_date until end_date.
    '''

    if cache_folder:
        cache = Cache(cache_folder)
    else:
        cache = None

    while start_date <= end_date:
        LOG.debug('Fetching data for %r', start_date)
        week_number = start_date.isocalendar()[1]
        url_args = [
            ('qsPage', 'data'),
            ('year', start_date.year),
            ('week', week_number),
        ]
        query = urlencode(url_args)
        url = 'http://www.pollen.lu/index.php?' + query
        if cache:
            data = cache.get(url)
        else:
            data = ''

        if not data:
            data = load_from_www(url)
            if cache:
                cache.put(url, data)

        if not data:
            LOG.error('Unable to get data from %r', url)
            continue

        data = parse_html(data)
        start_date = start_date + timedelta(weeks=1)
        for row in data:
            yield row


def as_list(row):
    return [row.date, row.lname, row.value]

