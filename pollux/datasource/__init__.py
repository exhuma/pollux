from datetime import date, datetime, timedelta
from io import BytesIO
from os.path import exists
from typing import List, Optional, Protocol, Tuple

import numpy as np  # type: ignore
import pandas as pd

import pollux.visualisations as vis
from pollux.cneg import PlotlyDict
from pollux.settings import Settings  # type: ignore
from pollux.stream import to_csv


def parse_date(str_date: str) -> str:
    month, day = str_date.split(";")
    obj = date(2000, int(month), int(day))
    return obj.strftime("%d. %B")


class DataSource(Protocol):
    def genera(self) -> List[str]:
        ...

    def between(
        self, start: datetime, end: datetime, genera: Optional[List[str]] = None
    ) -> pd.DataFrame:
        ...

    def recent(
        self, num_days: int = 7, genera: Optional[List[str]] = None
    ) -> pd.DataFrame:
        ...

    def heatmap(self, genus: str) -> PlotlyDict:
        ...

    def lineplot(self, genus: str) -> Tuple[bytes, str]:
        ...


def create_datasource(settings: Settings) -> DataSource:
    """
    Create a new data-source from the application settings
    """
    return PandasDS.from_filename(settings.filename)


class PandasDS:
    """
    A datasource based on Pandas
    """

    @staticmethod
    def from_filename(filename: str) -> "PandasDS":
        """
        Initialise a PandasDS source from a given filename. If the file does not
        exist, fetch the last month of data as initialisation.
        """
        if not exists(filename):
            now = datetime.now()
            to_csv(
                date(now.year, now.month - 1, 1),
                date(now.year, now.month, 31),
                filename,
            )
        return PandasDS(filename)

    def __init__(self, filename: str) -> None:
        self.data_frame = pd.read_csv(
            filename, index_col=["date"], parse_dates=["date"]
        )

    def genera(self) -> List[str]:
        return sorted(self.data_frame.columns)

    def between(
        self, start: datetime, end: datetime, genera: Optional[List[str]] = None
    ) -> pd.DataFrame:
        genera = genera or []
        subset = self.data_frame.loc[
            (self.data_frame.index >= start) & (self.data_frame.index <= end)
        ]
        return subset

    def recent(
        self, num_days: int = 7, genera: Optional[List[str]] = None
    ) -> pd.DataFrame:
        genera = genera or []
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

        data = {"z": data, "y": y, "x": x, "type": "heatmap"}
        return data

    def lineplot(self, genus: str) -> Tuple[bytes, str]:
        """
        Generate a lineplot as PNG image

        This is a "sandbox" function for quick tests.
        """
        df = pd.read_csv("data.csv")
        df["date"] = df["date"].apply(pd.to_datetime)
        df = df.set_index("date")
        fig = vis.lineplot(df, genus=genus)
        output = BytesIO()
        fig.savefig(output, format="png")
        data = output.getvalue()
        return (data, "image/png")
