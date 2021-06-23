import logging
from datetime import date, datetime, timedelta
from os import makedirs, unlink
from os.path import exists, join
from typing import Any, Generator, List
from urllib.parse import parse_qs, urlencode, urlsplit

from pollux import parse_html
from pollux.model import Datum

LOG = logging.getLogger(__name__)
CACHE_ENCODING = "utf8"


class Cache:
    def __init__(self, root: str) -> None:
        self.root = root
        if not exists(root):
            LOG.info("Creating cache dir %r", root)
            makedirs(root)

    def _url_to_filename(self, url: str) -> str:
        url_parts = urlsplit(url)
        query_data = parse_qs(url_parts.query)
        year = query_data["year"][0]
        week = query_data["week"][0]
        return join(self.root, "data-%s-%s.html" % (year, week))

    def get(self, url: str) -> str:
        LOG.debug("Fetching from cache: %r", url)
        filename = self._url_to_filename(url)
        if exists(filename):
            with open(filename, encoding=CACHE_ENCODING) as fp:
                data = fp.read()
        else:
            data = ""
        return data

    def put(self, url: str, data: str) -> None:
        LOG.debug("Storing to cache: %r", url)
        if not data:
            return
        filename = self._url_to_filename(url)
        if exists(filename):
            raise IOError("File %r exists!" % filename)
        with open(filename, "w", encoding=CACHE_ENCODING) as fp:
            try:
                fp.write(data)
                success = True
            except:
                breakpoint()
                LOG.debug("Unable to store data in cache.", exc_info=True)
                success = False
        # The "with" block will always create the file, even if storing data
        # fails. So we need to clean up if necessary.
        if not success and exists(filename):
            unlink(filename)


def load_from_www(url: str) -> str:
    LOG.debug("Fetching from %r", url)
    import requests

    response = requests.get(url)
    return response.text


def fetch_from(
    start_date: date, end_date: date = datetime.now().date(), cache_folder: str = ""
) -> Generator[Datum, None, None]:
    """
    Return a generator over each value starting from start_date until end_date.
    """

    cache = None
    if cache_folder:
        cache = Cache(cache_folder)

    while start_date <= end_date:
        LOG.info(
            "Fetching data for %s (Week #%s)", start_date, start_date.strftime("%U")
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
