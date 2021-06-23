"""
Visualisations/Graphs for the project
"""
from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from pandas import DataFrame


def heatmap(dataframe: DataFrame, genus: str = "Gramineae") -> Figure:
    """
    Generate a heatmap for the given genus of pollen
    """
    filtered = dataframe.filter([genus])
    filtered["year"] = filtered.index.year
    filtered["day"] = filtered.index.map(lambda z: (z.month, z.day))

    yearly = filtered.pivot(index="year", columns="day", values=genus)
    figure = plt.figure(figsize=(32, 20))
    sns.heatmap(yearly)
    return figure


def lineplot(
    dataframe: DataFrame,
    genus: str = "Gramineae",
    start: datetime = datetime(1996, 1, 1),
    end: Optional[datetime] = None,
) -> Figure:
    """
    Draws a simple line-plot
    """
    filtered = dataframe.filter([genus])
    if end:
        timespan = (filtered.index < end) & (filtered.index >= start)
    else:
        timespan = filtered.index >= start
    data = filtered.loc[timespan]
    figure = plt.figure(figsize=(32, 20))
    sns.lineplot(x=data.index, y="Gramineae", data=data)
    return figure
