"""
Helper functions to transform data into payloads as requested by the client
"""
from typing import Any, Dict, List

from pandas import DataFrame

PlotlyDict = Dict[str, Dict[str, Any]]


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
