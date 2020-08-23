from datetime import date, datetime, timedelta
from typing import Any, Dict, List

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

PlotlyDict = Dict[str, Dict[str, Any]]


def parse_date(str_date: str) -> str:
    month, day = str_date.split(";")
    obj = date(2000, int(month), int(day))
    return obj.strftime("%d. %B")


class DataSource:
    @staticmethod
    def default() -> "DataSource":
        return PandasDS()


class PandasDS(DataSource):
    def __init__(self) -> None:
        self.data_frame = pd.read_csv(
            "data.csv", index_col=["date"], parse_dates=["date"]
        )

    def genera(self) -> List[str]:
        return sorted(self.data_frame.columns)

    def between(self, start: datetime, end: datetime, genera: str = "") -> PlotlyDict:
        subset = self.data_frame.loc[
            (self.data_frame.index >= start) & (self.data_frame.index <= end)
        ]
        genera = genera or subset
        output = {}
        for genus in genera:
            x = [date.isoformat() for date in subset[genus].index]
            y = list(subset[genus])
            output[genus] = {
                "x": x,
                "y": y,
                "name": genus,
                "type": "bar",
            }
        return output

    def recent(self, num_days: int = 7, genera: str = "") -> PlotlyDict:
        now = datetime.now()
        start = now - timedelta(days=num_days)
        return self.between(start, now, genera=genera)

    def heatmap(self, genus: str) -> PlotlyDict:
        self.data_frame["year"] = self.data_frame.index.year
        self.data_frame["date2"] = self.data_frame.index.strftime("%m;%d")
        pivoted = pd.pivot_table(
            self.data_frame,
            values=genus,
            index="year",
            columns="date2",
            aggfunc=np.sum,
            fill_value=-1,
        )

        data = []
        y = []
        x = []
        for index, row in pivoted.iterrows():
            year_values = list(row)
            if not x:
                x = [parse_date(cell) for cell in row.index]
            y.append(str(index))
            data.append(year_values)

        data = {
            "z": data,
            "y": y,
            "x": x,
            "type": "heatmap"
        }
        return data
