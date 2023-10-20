from general_analytics_framwork.base_processes import AbstractComponent
from general_analytics_framwork.base_processes import (
    SequenceProcess,
    ParallelProcess
)
from general_analytics_framwork.iterators import (
    DataSequenceIterator
)
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot


class DataPlotter(AbstractComponent):

    def __init__(self, title, fig_size, x_label, y_label, iterator=None):
        assert len(fig_size) == 2, "fig_size parameter should be a list of " \
                                   "two integers"
        self.title = title
        self.fig_size = (fig_size[0], fig_size[1])
        self.x_label = x_label
        self.y_label = y_label
        super().__init__(iterator=iterator)

    def run(self, data):
        self.iterator.iterate(self.plot, data)

    def plot(self, data):
        raise NotImplementedError


class TimeseriesPlotter(DataPlotter):

    AVAILABLE_ITERATORS = {
        "data_sequence": DataSequenceIterator
    }

    def plot(self, time_series_dataset):
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=time_series_dataset.dates, y=time_series_dataset.y_data)
        plt.title(f"{self.title}{time_series_dataset.series_id}")
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.xticks(rotation=45)
        plt.show()


class BarGraphPlotter(DataPlotter):

    def run(self, time_series_list):
        data = {
            "series_id": [ts.series_id for ts in time_series_list],
            "mean_y": [pd.Series(ts.y_data).mean() for ts in
                             time_series_list]
        }
        df = pd.DataFrame(data)
        plt.figure(figsize=self.fig_size)
        sns.barplot(x="series_id", y="mean_y", data=df)
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.show()


class AutocorrelationPlotter(DataPlotter):

    AVAILABLE_ITERATORS = {
        "data_sequence": DataSequenceIterator
    }

    def plot(self, time_series_dataset):
        plt.figure(figsize=self.fig_size)
        autocorrelation_plot(time_series_dataset.y_data)
        plt.title(
            f"{self.title} Autocorrelation: {time_series_dataset.series_id}"
        )
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.show()


class DataVisualisationProcess(ParallelProcess):
    AVAILABLE_STRATEGIES = {
        "time_series": TimeseriesPlotter,
        "bar_graph": BarGraphPlotter,
        "auto_correlation": AutocorrelationPlotter
    }
