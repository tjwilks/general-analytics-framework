from general_analytics_framwork.base_processes import (
    AbstractNode,
    AbstractComponent
)
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot


class DataPlotter(AbstractComponent):

    def __init__(self, title, fig_size, x_label, y_label):
        assert len(fig_size) == 2, "fig_size parameter should be a list of " \
                                   "two integers"
        self.title = title
        self.fig_size = (fig_size[0], fig_size[1])
        self.x_label = x_label
        self.y_label = y_label
        self.process = self.plot

    def run(self, data):
        output = []
        for element in data:
            element_output = self.process(element)
            element_output.show()
            output.append(element_output)
        return output

    def plot(self, data):
        raise NotImplementedError


class TimeseriesPlotter(DataPlotter):

    def plot(self, time_series_dataset):
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(
            x=time_series_dataset.dates,
            y=time_series_dataset.y_data,
            ax=ax
        )
        ax.set_title(f"{self.title}{time_series_dataset.series_id}")
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        ax.set_xticklabels(labels=ax.get_xticklabels(), rotation=45)
        return fig


class AutocorrelationPlotter(DataPlotter):

    def plot(self, time_series_dataset):
        fig, ax = plt.subplots(figsize=self.fig_size)
        autocorrelation_plot(time_series_dataset.y_data, ax=ax)
        ax.set_title(
            f"{self.title} Autocorrelation: {time_series_dataset.series_id}"
        )
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        return fig


class BarGraphPlotter(DataPlotter):

    def run(self, time_series_list):
        data = pd.DataFrame({
            "series_id": [ts.series_id for ts in time_series_list],
            "mean_y": [pd.Series(ts.y_data).mean() for ts in time_series_list]
        })
        plot = self.plot(data)
        return plot

    def plot(self, data):
        fig, ax = plt.subplots(figsize=self.fig_size)
        sns.barplot(x="series_id", y="mean_y", data=data, ax=ax)
        ax.set_title(self.title)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        return fig


