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


class ForecastGraphPlotter(DataPlotter):

    def __init__(
            self,
            title,
            fig_size,
            x_label,
            y_label,
            start_index=None,
            end_index=None
    ):
        self.start_index = start_index
        self.end_index = end_index
        super().__init__(title, fig_size, x_label, y_label)

    def run(self, backtest_datasets):
        for backtest_dataset in backtest_datasets:
            self.plot_windows(backtest_dataset)

    def plot_windows(self, backtest_dataset):
        start_index = self.start_index if self.start_index else 1
        end_index = self.end_index if self.end_index else \
            max(backtest_dataset.predictions.keys())
        window_indexes_to_plot = range(start_index, end_index)
        for window_index in window_indexes_to_plot:
            backtest_dataset.window.move_to_index(window_index)
            self.plot(backtest_dataset)

    def plot(self, backtest_dataset):
        fig, ax = plt.subplots(figsize=self.fig_size)
        sns.lineplot(
            x=backtest_dataset.get_data("dates", "train"),
            y=backtest_dataset.get_data("y", "train"),
            color="black",
            linewidth=1.25
        )
        get_test_period_data = lambda requested_data: \
            [backtest_dataset.get_data(requested_data, "train")[-1]] + \
            backtest_dataset.get_data(requested_data, "test")
        sns.lineplot(
            x=get_test_period_data("dates"),
            y=get_test_period_data("y"),
            color="black",
            linestyle="dashed",
            linewidth=1.25
        )
        train_period_last_y_point = backtest_dataset.get_data("y", "train")[-1]

        forecasts_data = pd.DataFrame({
            model.get_reference(): [train_period_last_y_point, *prediction]
            for model, prediction in
            backtest_dataset.predictions[backtest_dataset.window.index].items()
        })
        forecasts_data['date'] = get_test_period_data("dates")
        forecasts_data = pd.melt(
            forecasts_data,
            id_vars=['date'],
            var_name='model',
            value_name='forecast'
        )
        sns.lineplot(
            x='date',
            y='forecast',
            hue="model",
            data=forecasts_data,
            linewidth=1.5
        )
        plt.axvline(
            x=backtest_dataset.get_data("dates", "train")[-1],
            linestyle='--',
            color='red'
        )
        ax.set_title(
            f"{self.title} - "
            f"ID: {backtest_dataset.time_series_dataset.series_id}, "
            f"Window: {backtest_dataset.window.index}")
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        fig.show()
        return fig, ax
