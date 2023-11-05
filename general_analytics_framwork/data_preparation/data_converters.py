from general_analytics_framwork.base_processes import AbstractComponent
from general_analytics_framwork.datasets import (
    TimeseriesDataset, TimeseriesBacktestDataset, ResultsDataset
)
from abc import abstractmethod

class AbstractDataConverter(AbstractComponent):

    def run(self, data):
        output = []
        for element in data:
            element_output = self.convert(element)
            output.append(element_output)
        return output

    @abstractmethod
    def convert(self, element):
        raise NotImplementedError



class TimeseriesConverter(AbstractDataConverter):

    def __init__(self, series_id_col, date_col, y_col, regressor_cols, date_parser):
        self.series_id_col = series_id_col
        self.date_col = date_col
        self.y_col = y_col
        self.regressor_cols = regressor_cols
        self.date_parser = date_parser

    def run(self, data):
        output = []
        for series_id in data[self.series_id_col].unique():
            element = data[data[self.series_id_col] == series_id]
            output_element = self.convert(series_id, element)
            output.append(output_element)
        return output

    def convert(self, series_id, element):
        time_series_dataset = TimeseriesDataset(
            series_id=series_id,
            dates=element[self.date_col].to_list(),
            y_data=element[self.y_col].to_list(),
            regressor_data={
                col: element[col] for col in self.regressor_cols
            },
            date_parser=self.date_parser
        )
        return time_series_dataset


class TimeseriesBacktestConverter(AbstractDataConverter):

    def __init__(self, train_window_length, max_test_window_length):
        self.train_window_length = train_window_length
        self.max_test_window_length = max_test_window_length

    def convert(self, data):
        data = TimeseriesBacktestDataset(
            time_series_dataset=data,
            train_window_length=self.train_window_length,
            max_test_window_length=self.max_test_window_length
        )
        return data


class BacktestResultsConverter(AbstractDataConverter):

    def __init__(self, error_function):
        self.error_function = error_function

    def convert(self, data):
        data = ResultsDataset(
            backtest_dataset=data,
            error_function=self.error_function
        )
        return data