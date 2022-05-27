"""
This module contains unit-tests for the HTTP API of pollux
"""

from contextlib import contextmanager
from datetime import datetime
from io import BytesIO, StringIO
from typing import Any, Iterable, Tuple
from unittest.mock import create_autospec, patch

from flask import Flask, Response, appcontext_pushed, g
from flask.testing import FlaskClient
from pytest import fixture
from werkzeug.datastructures import FileStorage

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
    app.config["AUTH_FILE"] = "users.json.dist"
    with set_datasource(app, mock_ds):
        client = app.test_client()
        yield client, mock_ds


def test_root(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Test that we get something non-errorish from the root URL
    """
    client, _ = fixture_objects
    response = client.get("/")
    assert response.status_code == 200


def test_lineplot(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Ensure that the call to /graph/lineplot works
    """
    client, datasource = fixture_objects
    datasource.lineplot.return_value = (
        b"example-bytes",
        "application/octet-stream",
    )
    response: Response = client.get("/graph/lineplot")
    assert response.status_code == 200
    datasource.lineplot.assert_called_with()
    assert response.data == b"example-bytes"
    assert response.content_type == "application/octet-stream"


def test_recent(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Ensure that the call to /recent works
    """
    client, datasource = fixture_objects
    response: Response = client.get(
        "/recent", query_string={"genus": ["genus-1", "genus-2"]}
    )
    assert response.status_code == 200
    datasource.recent.assert_called_with(
        num_days=7, genera=["genus-1", "genus-2"]
    )
    assert response.json == []  # TODO: Mock some real data


def test_between(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Ensure that the call to /between works
    """
    client, datasource = fixture_objects
    response: Response = client.get(
        "/between/2021-01-01/2022-12-31",
        query_string={"genus": ["genus-1", "genus-2"]},
    )
    assert response.status_code == 200
    datasource.between.assert_called_with(
        datetime(2021, 1, 1, 0, 0),
        datetime(2022, 12, 31, 0, 0),
        genera=["genus-1", "genus-2"],
    )
    assert response.json == []  # TODO: Mock some real data


def test_genera(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Ensure that the call to /genera works
    """
    client, datasource = fixture_objects
    datasource.genera.return_value = ["genus-1", "genus-2"]
    response: Response = client.get("/genera")
    assert response.status_code == 200
    datasource.genera.assert_called_with()
    assert response.json == ["genus-1", "genus-2"]


def test_heatmap(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Ensure that the call to /heatmap works
    """
    client, datasource = fixture_objects
    datasource.heatmap.return_value = ["sentinel-value"]
    response: Response = client.get("/heatmap/genus-1")
    assert response.status_code == 200
    datasource.heatmap.assert_called_with("genus-1")
    assert response.json == ["sentinel-value"]


def test_upload(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    ensure that we can upload files
    """
    client, _ = fixture_objects

    auth_response = client.post(
        "/auth", json={"username": "john.doe", "password": "supersecret"}
    )

    with patch("pollux.blueprint.main._store_file") as store_file:
        response: Response = client.post(
            "/upload",
            data={
                "example-file.csv": (
                    "tests/data/test-upload.csv",
                    "tests/data/test-upload.csv",
                    BytesIO(b"hello-world"),
                )
            },
            headers={"Authorization": f"jwt {auth_response.json['token']}"},
        )
        assert response.status_code == 200, response.data
        assert len(store_file.mock_calls) == 1
        assert store_file.mock_calls[0][1][0] == "example-file.csv"


def test_upload_unauthorised(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    ensure that we are not allowed to upload files if we do not have the
    permission
    """
    client, _ = fixture_objects

    auth_response = client.post(
        "/auth", json={"username": "jane.doe", "password": "supersecret"}
    )

    response: Response = client.post(
        "/upload",
        data={
            "example-file.csv": (
                "tests/data/test-upload.csv",
                "tests/data/test-upload.csv",
                BytesIO(b"hello-world"),
            )
        },
        headers={"Authorization": f"jwt {auth_response.json['token']}"},
    )
    assert response.status_code == 403, response.data


def test_invalid_token(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Ensure that the call to /recent works
    """
    client, _ = fixture_objects
    response: Response = client.get(
        "/recent", headers={"Authorization": "Basic foo:bar"}
    )
    assert response.status_code == 401


def test_cors_headers(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    Ensure that responses contain CORS headers
    """
    client, _ = fixture_objects
    response: Response = client.get("/")
    assert response.headers["Access-Control-Allow-Origin"] == "*"
    assert (
        response.headers["Access-Control-Allow-Headers"]
        == "Content-Type, Authorization"
    )


def test_auth_no_permissions(fixture_objects: Tuple[FlaskClient, PandasDS]):
    """
    If a user has no permissions, return an unauthorized
    """
    client, _ = fixture_objects

    auth_response = client.post(
        "/auth", json={"username": "max.mustermann", "password": "supersecret"}
    )
    assert auth_response.status_code == 401, auth_response.data
