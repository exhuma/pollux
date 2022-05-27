"""
This module contains unit-tests for the HTTP API of pollux
"""

from flask import Response
from flask.testing import FlaskClient
from pytest import fixture

from pollux.api import make_app


@fixture
def client() -> FlaskClient:
    """
    Provide a Flask test-client
    """
    app = make_app()
    return app.test_client()


def test_root(client: FlaskClient):
    """
    Test that we get something non-errorish from the root URL
    """
    response = client.get("/")
    assert response.status_code == 200


def test_recent(client: FlaskClient):
    """
    Ensure that the call to /recent works
    """
    response: Response = client.get("/recent")
    assert response.status_code == 200
