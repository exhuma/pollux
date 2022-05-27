import logging
from os import makedirs, unlink
from os.path import exists, join
from typing import Optional
from urllib.parse import parse_qs, urlsplit

LOG = logging.getLogger(__name__)
CACHE_ENCODING = "utf8"


class DiskIO:
    """
    Abstraction for low-level file-access to provide an injection point for
    unit-tests
    """

    def create_folder_if_missing(
        self, folder_name: str
    ) -> None:  # pragma: no cover
        """
        Create a new folder if it is missing, otherwise do nothing
        """
        if exists(folder_name):
            return
        LOG.info("Creating cache dir %r", folder_name)
        makedirs(folder_name)

    def read_text(
        self, filename: str, encoding: str
    ) -> str:  # pragma: no cover
        """
        If the file exists return its contents as string, otherwise return an
        empty string.
        """
        if not exists(filename):
            return ""

        with open(filename, encoding=encoding) as fptr:
            return fptr.read()

    def write_text(
        self, filename: str, data: str, encoding: str
    ) -> bool:  # pragma: no cover
        """
        Write content to a text-file and return wether it was successful or not,
        preventing exceptions.
        """
        if exists(filename):
            raise IOError(f"File {filename} exists!")
        with open(filename, "w", encoding=encoding) as fptr:
            try:
                fptr.write(data)
                success = True
            except:  # pylint: disable=bare-except
                LOG.debug("Unable to store data in cache.", exc_info=True)
                success = False
        # The "with" block will always create the file, even if storing data
        # fails. So we need to clean up if necessary.
        if not success and exists(filename):
            unlink(filename)
        return success


class Cache:
    """
    A simple HTTP cache which stores responses indefintely on disk.

    Apart from removing the files from disk manually, there is no way to clear
    the cache.
    """

    def __init__(self, root: str, diskio: Optional[DiskIO] = None) -> None:
        self.root = root

        if diskio is None:
            self._diskio = DiskIO()
        else:
            self._diskio = diskio

        self._diskio.create_folder_if_missing(root)

    def _url_to_filename(self, url: str) -> str:
        url_parts = urlsplit(url)
        query_data = parse_qs(url_parts.query)
        year = query_data["year"][0]
        week = query_data["week"][0]
        return join(self.root, "data-%s-%s.html" % (year, week))

    def get(self, url: str) -> str:
        LOG.debug("Fetching from cache: %r", url)
        filename = self._url_to_filename(url)
        data = self._diskio.read_text(filename, CACHE_ENCODING)
        return data

    def put(self, url: str, data: str) -> bool:
        LOG.debug("Storing to cache: %r", url)
        if not data:
            return True
        filename = self._url_to_filename(url)
        return self._diskio.write_text(filename, data, CACHE_ENCODING)
