import pandas as pd
from datetime import datetime, timedelta


class DataSource:

    @staticmethod
    def default():
        return PandasDS()


class PandasDS:

    def __init__(self):
        self.data_frame = pd.read_csv(
            'foo',
            index_col=['date'],
            parse_dates=['date'])

    def genera(self):
        return sorted(self.data_frame.columns)

    def between(self, start, end, genera=None):
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

    def recent(self, num_days=7, genera=None):
        now = datetime.now()
        start = now - timedelta(days=num_days)
        return this.between(start, now, genera=genera)
