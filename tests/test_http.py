"""
This module contains unit-tests for the HTTP API of pollux
"""

from datetime import datetime
from io import BytesIO
from typing import Any, Iterable, Tuple
from unittest.mock import create_autospec, patch

import pytest
from fastapi import Response
from fastapi.testclient import TestClient
from pytest import fixture

from pollux.api import get_settings, make_app
from pollux.datasource import PandasDS
from pollux.dependencies import get_data_source
from pollux.settings import Settings


def get_test_settings() -> Settings:
    """
    Return settings usable during testing
    """
    output = Settings()
    output.auth_file = "users.json.dist"
    return output


@fixture
def fixture_objects() -> Iterable[Tuple[Any, PandasDS]]:
    """
    Provide a Any test-client
    """
    mock_ds = create_autospec(PandasDS)
    app = make_app()
    app.dependency_overrides[get_settings] = get_test_settings
    app.dependency_overrides[get_data_source] = lambda: mock_ds
    client = TestClient(app)
    yield client, mock_ds


def test_root(fixture_objects: Tuple[TestClient, PandasDS]):
    """
    Test that we get something non-errorish from the root URL
    """
    client, _ = fixture_objects
    response = client.get("/")
    assert response.status_code == 200


def test_lineplot(fixture_objects: Tuple[TestClient, PandasDS]):
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
    assert response.content == b"example-bytes"
    assert response.headers["Content-Type"] == "application/octet-stream"


def test_recent(fixture_objects: Tuple[TestClient, PandasDS]):
    """
    Ensure that the call to /recent works
    """
    client, datasource = fixture_objects
    response: Response = client.get(
        "/recent", params={"genus": ["genus-1", "genus-2"]}
    )
    assert response.status_code == 200
    datasource.recent.assert_called_with(
        num_days=7, genera=["genus-1", "genus-2"]
    )
    assert response.json() == []  # TODO: Mock some real data


def test_between(fixture_objects: Tuple[TestClient, PandasDS]):
    """
    Ensure that the call to /between works
    """
    client, datasource = fixture_objects
    response: Response = client.get(
        "/between/2021-01-01/2022-12-31",
        params={"genus": ["genus-1", "genus-2"]},
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 200
    datasource.between.assert_called_with(
        datetime(2021, 1, 1, 0, 0),
        datetime(2022, 12, 31, 0, 0),
        genera=["genus-1", "genus-2"],
    )
    assert response.json() == []  # TODO: Mock some real data


def test_genera(fixture_objects: Tuple[TestClient, PandasDS]):
    """
    Ensure that the call to /genera works
    """
    client, datasource = fixture_objects
    datasource.genera.return_value = ["genus-1", "genus-2"]
    response: Response = client.get("/genera")
    assert response.status_code == 200
    datasource.genera.assert_called_with()
    assert response.json() == ["genus-1", "genus-2"]


def test_heatmap(fixture_objects: Tuple[TestClient, PandasDS]):
    """
    Ensure that the call to /heatmap works
    """
    client, datasource = fixture_objects
    datasource.heatmap.return_value = ["sentinel-value"]
    response: Response = client.get("/heatmap/genus-1")
    assert response.status_code == 200
    datasource.heatmap.assert_called_with("genus-1")
    assert response.json() == ["sentinel-value"]


@pytest.mark.skip("TODO")
def test_upload(fixture_objects: Tuple[TestClient, PandasDS]):
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
            headers={"Authorization": f"jwt {auth_response.json()['token']}"},
        )
        assert response.status_code == 200, response.content
        assert len(store_file.mock_calls) == 1
        assert store_file.mock_calls[0][1][0] == "example-file.csv"


@pytest.mark.skip("TODO")
def test_upload_unauthorised(fixture_objects: Tuple[TestClient, PandasDS]):
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
            "file": (
                "tests/data/test-upload.csv",
                "tests/data/test-upload.csv",
                BytesIO(b"hello-world"),
            )
        },
        headers={"Authorization": f"jwt {auth_response.json()['token']}"},
    )
    assert response.status_code == 403, response.content


def test_invalid_token(fixture_objects: Tuple[TestClient, PandasDS]):
    """
    Ensure that the call to /recent works
    """
    client, _ = fixture_objects
    response: Response = client.get(
        "/recent", headers={"Authorization": "Basic foo:bar"}
    )
    assert response.status_code == 401


def test_cors_headers(fixture_objects: Tuple[TestClient, PandasDS]):
    """
    Ensure that responses contain CORS headers
    """
    client, _ = fixture_objects
    response: Response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:8080",
            "Content-Type": "application/json",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == "http://localhost:8080"
    )
    assert "Authorization" in response.headers["Access-Control-Allow-Headers"]


def test_auth_no_permissions(fixture_objects: Tuple[TestClient, PandasDS]):
    """
    If a user has no permissions, return an unauthorized
    """
    client, _ = fixture_objects

    auth_response = client.post(
        "/auth", json={"username": "max.mustermann", "password": "supersecret"}
    )
    assert auth_response.status_code == 401, auth_response.content
