import logging
from os import makedirs, unlink
from os.path import exists, join
from urllib.parse import parse_qs, urlsplit

LOG = logging.getLogger(__name__)
CACHE_ENCODING = "utf8"


class Cache:
    """
    A simple HTTP cache which stores responses indefintely on disk.

    Apart from removing the files from disk manually, there is no way to clear
    the cache.
    """

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
