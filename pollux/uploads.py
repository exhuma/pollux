"""
This module contains everything related to uploading new files to the service
"""

from pathlib import Path
from posixpath import splitext


def allowed_file(filename: str) -> bool:
    """
    Return true if a file can be accepted as an upload
    """
    _, ext = splitext(filename)
    return ext.lower() in {".csv"}
