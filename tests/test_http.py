"""
This module contains unit-tests for the HTTP API of pollux
"""

from contextlib import contextmanager
from typing import Any, Iterable, Tuple
from unittest.mock import create_autospec

from flask import Flask, Response, appcontext_pushed, g
from flask.testing import FlaskClient
from pytest import fixture

from pollux.api import make_app
from pollux.datasource import PandasDS


@contextmanager
def set_datasource(app: Flask, data_source: PandasDS):
    def handler(sender: Any, **kwargs: Any):
        g.data_source = data_source

    with appcontext_pushed.connected_to(handler, app):
        yield


@fixture
def fixture_objects() -> Iterable[Tuple[FlaskClient, PandasDS]]:
    """
    Provide a Flask test-client
    """
    mock_ds = create_autospec(PandasDS)
    app = make_app()
    with set_datasource(app, mock_ds):
        client = app.test_client()
        yield client, mock_ds


def test_root(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Test that we get something non-errorish from the root URL
    """
    client, datasource = fixture_objects
    response = client.get("/")
    assert response.status_code == 200


def test_recent(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Ensure that the call to /recent works
    """
    client, datasource = fixture_objects
    response: Response = client.get("/recent")
    assert response.status_code == 200
