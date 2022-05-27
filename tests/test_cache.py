"""
This module contains unit-tests for the local caching implementation
"""
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

from unittest.mock import create_autospec

from pollux.cache import Cache, DiskIO


def test_default_diskio():
    """
    Ensure that we get a proper DiskIO instance when not passing any args
    """
    cache = Cache("fake-root")
    assert isinstance(cache._diskio, DiskIO)


def test_url_to_filename():
    """
    Test that we are correctly transforming URLs to filenames
    """
    diskio = create_autospec(DiskIO)
    cache = Cache("example-folder", diskio=diskio)
    result = cache._url_to_filename("https://foo/bar?year=2022&week=12")
    assert result == "example-folder/data-2022-12.html"


def test_get():
    """
    Test that we can open files on disk
    """
    diskio = create_autospec(DiskIO)
    diskio.read_text.return_value = "sentinel-value"
    cache = Cache("example-folder", diskio=diskio)
    result = cache.get("http://example.com?year=2022&week=42")
    assert result == "sentinel-value"
    diskio.read_text.assert_called_with(
        "example-folder/data-2022-42.html", "utf8"
    )


def test_write():
    """
    Test that we can write files to disk
    """
    diskio = create_autospec(DiskIO)
    diskio.write_text.return_value = True
    cache = Cache("example-folder", diskio=diskio)
    result = cache.put("http://example.com?year=2022&week=42", "sample-data")
    assert result is True
    diskio.write_text.assert_called_with(
        "example-folder/data-2022-42.html", "sample-data", "utf8"
    )


def test_write_nodata():
    """
    If we pass no data, no disk-write should occur
    """
    diskio = create_autospec(DiskIO)
    diskio.write_text.return_value = True
    cache = Cache("example-folder", diskio=diskio)
    result = cache.put("http://example.com?year=2022&week=42", "")
    assert result is True
    diskio.write_text.assert_not_called()
