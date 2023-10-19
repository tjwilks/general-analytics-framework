from general_analytics_framwork.base_processes import AbstractComponent
from old_code.backtesting_central_analysis_subprocess_mediator import (
    TimeseriesDataset, TimeseriesBacktestDataset
)


class TimeseriesConverter(AbstractComponent):

    def __init__(self, series_id_col, date_col, y_col, regressor_cols, date_parser):
        self.series_id_col = series_id_col
        self.date_col = date_col
        self.y_col = y_col
        self.regressor_cols = regressor_cols
        self.date_parser = date_parser

    def run(self, data):
        time_series_datasets = []
        for series_id in data[self.series_id_col].unique():
            series_id_data = data[data[self.series_id_col] == series_id]
            series_id_dataset = TimeseriesDataset(
                series_id=series_id,
                dates=series_id_data[self.date_col].to_list(),
                y_data=series_id_data[self.y_col].to_list(),
                regressor_data={
                    col: series_id_data[col] for col in self.regressor_cols
                },
                date_parser=self.date_parser
            )
            time_series_datasets.append(series_id_dataset)
        return time_series_datasets


class TimeseriesBacktestConverter(AbstractComponent):

    def __init__(self, train_window_length, max_test_window_length):
        self.train_window_length = train_window_length
        self.max_test_window_length = max_test_window_length

    def run(self, data):
        time_series_backtest_dataset_list = []
        for time_series_dataset in data:
            time_series_backtest_dataset = TimeseriesBacktestDataset(
                time_series_dataset=time_series_dataset,
                train_window_length=self.train_window_length,
                max_test_window_length=self.max_test_window_length
            )
            time_series_backtest_dataset_list.append(
                time_series_backtest_dataset
            )
        return time_series_backtest_dataset_list
