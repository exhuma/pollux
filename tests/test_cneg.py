"""
This module contains unit-tests for content-negotiation
"""

from typing import Dict, List

import pytest

from pollux.cneg import AcceptHeaderItem, best_accept_match


@pytest.mark.parametrize(
    "accept_header, supported_types, expected_match",
    [
        ("*/*", ["application/json", "text/plain"], "application/json"),
        ("text/plain", ["application/json", "text/plain"], "text/plain"),
        ("a/b; q=0.2, b/c; q=0.5", ["a/b", "b/c", "c/d"], "b/c"),
    ],
)
def test_best_accept_match(
    accept_header: str, supported_types: List[str], expected_match: str
):
    """
    Test that we are capable of retrieving a good fit for a media-type for the
    client.
    """
    result = best_accept_match(accept_header, supported_types)
    assert result == expected_match


@pytest.mark.parametrize(
    [
        "raw_value",
        "expected_mt",
        "expected_args",
        "expected_quality",
        "expected_accept_args",
    ],
    [
        (
            "a/b; foo=bar; q=0.5; foo2=bar2",
            "a/b",
            {"foo": "bar"},
            0.5,
            {"foo2": "bar2"},
        ),
        ("a/b", "a/b", {}, 1.0, {}),
        ("a/b; q=0.5; foo2=bar2", "a/b", {}, 0.5, {"foo2": "bar2"}),
        ("a/b; foo=bar; q=0.5", "a/b", {"foo": "bar"}, 0.5, {}),
    ],
)
def test_accept_item(
    raw_value: str,
    expected_mt: str,
    expected_args: Dict[str, str],
    expected_quality: float,
    expected_accept_args: Dict[str, str],
):
    """
    Ensure we are properly parsing accept header items
    """
    result = AcceptHeaderItem(raw_value)
    assert result.without_args == expected_mt
    assert result.args == expected_args
    assert result.quality == expected_quality
    assert result.accept_args == expected_accept_args
