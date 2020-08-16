from datetime import datetime, timedelta
from typing import List, Dict, Any

import pandas as pd  # type: ignore


PlotlyDict = Dict[str, Dict[str, Any]]


class DataSource:

    @staticmethod
    def default() -> "DataSource":
        return PandasDS()


class PandasDS(DataSource):

    def __init__(self) -> None:
        self.data_frame = pd.read_csv(
            'data.csv',
            index_col=['date'],
            parse_dates=['date'])

    def genera(self) -> List[str]:
        return sorted(self.data_frame.columns)

    def between(
        self,
        start: datetime,
        end: datetime,
        genera: str = ''
    ) -> PlotlyDict:
        subset = self.data_frame.loc[
            (self.data_frame.index >= start) &
            (self.data_frame.index <= end)
        ]
        genera = genera or subset
        output = {}
        for genus in genera:
            x = [date.isoformat() for date in subset[genus].index]
            y = list(subset[genus])
            output[genus] = {
                'x': x,
                'y': y,
                'name': genus,
                'type': 'bar',
            }
        return output

    def recent(self, num_days: int = 7, genera: str = '') -> PlotlyDict:
        now = datetime.now()
        start = now - timedelta(days=num_days)
        return self.between(start, now, genera=genera)
