"""
Helper functions to transform data into payloads as requested by the client
"""
from dataclasses import dataclass
from typing import Any, Dict, List

from pandas import DataFrame

PlotlyDict = Dict[str, Dict[str, Any]]


@dataclass
class KeyValue:
    key: str
    value: str


def parse_kv(keyvalue: str) -> KeyValue:
    """
    Convert a "foo=bar" string into a proper Python dataclass

    >>> parse_kv("foo=bar")
    KeyValue(key="foo", value="bar")
    """
    key, _, value = keyvalue.partition("=")
    return KeyValue(key.strip(), value.strip())


class AcceptHeaderItem:
    """
    Represents an item of the HTTP Accept Header
    """

    def __init__(self, raw_value: str) -> None:
        self.raw_value = raw_value
        without_args, _, rest = raw_value.partition(";")
        mappings = [parse_kv(item) for item in rest.split(";") if item.strip()]
        self.without_args = without_args
        self.args: Dict[str, str] = {}
        self.quality = 1.0
        self.accept_args: Dict[str, str] = {}
        target = self.args
        for mapping in mappings:
            if mapping.key == "q":
                target = self.accept_args
                self.quality = float(mapping.value)
                continue
            target[mapping.key] = mapping.value

    def as_content_type(self) -> str:
        """
        Return the item without accept-header arguments
        """
        if self.args:
            args = "; ".join(
                f"{key}={value}" for key, value in self.args.items()
            )
            return f"{self.without_args}; {args}"
        return self.without_args

    def __repr__(self) -> str:
        return f"AcceptHeaderItem({self.raw_value!r})"


def make_plotly_dict(dataframe: DataFrame, genera: List[str]) -> PlotlyDict:
    output = {}
    for genus in genera:
        x = [date.isoformat() for date in dataframe[genus].index]
        y = list(dataframe[genus])
        output[genus] = {
            "x": x,
            "y": y,
            "name": genus,
            "type": "bar",
        }
    return output


def make_plain_dict(dataframe: DataFrame) -> Dict[str, Any]:
    """
    Convert to a simple application-specific dictionary
    """
    output = []
    for index, data in dataframe.iterrows():
        tmp = {
            "date": index.to_pydatetime().date().isoformat(),
        }
        for key, value in data.items():
            tmp[key] = value
        output.append(tmp)
    return output


def best_accept_match(
    accept_types: str, supported_mediatypes: List[str]
) -> str:
    """
    Given a request "accept" header value and a set of supported media types,
    return the best possible match for the client
    """
    all_types = {
        AcceptHeaderItem(item.strip()) for item in accept_types.split(",")
    }
    sorted_types = sorted(all_types, key=lambda item: -item.quality)
    for requested_type in sorted_types:
        if requested_type.without_args == "*/*":
            return supported_mediatypes[0]
        if requested_type.without_args in supported_mediatypes:
            return requested_type.as_content_type()
    return ""
