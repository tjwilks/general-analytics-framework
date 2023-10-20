from general_analytics_framwork.base_processes import AbstractComponent
from general_analytics_framwork.datasets import (
    TimeseriesDataset, TimeseriesBacktestDataset
)
from general_analytics_framwork.iterators import (
    DataframeAggregationSequenceIterator, DataAggregationSequenceIterator
)


class DataConverter(AbstractComponent):

    def run(self, data):
        output = self.iterator.iterate(self.convert, data)
        return output


class TimeseriesConverter(DataConverter):

    AVAILABLE_ITERATORS = {
        "dataframe_aggregation_sequence": DataframeAggregationSequenceIterator
    }

    def __init__(self, series_id_col, date_col, y_col, regressor_cols, date_parser, iterator):
        self.series_id_col = series_id_col
        self.date_col = date_col
        self.y_col = y_col
        self.regressor_cols = regressor_cols
        self.date_parser = date_parser
        self.iterator = iterator


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


class TimeseriesBacktestConverter(DataConverter):
    AVAILABLE_ITERATORS = {
        "data_aggregation_sequence": DataAggregationSequenceIterator
    }

    def __init__(self, train_window_length, max_test_window_length, iterator):
        self.train_window_length = train_window_length
        self.max_test_window_length = max_test_window_length
        self.iterator = iterator

    def convert(self, data):
        time_series_backtest_dataset = TimeseriesBacktestDataset(
            time_series_dataset=data,
            train_window_length=self.train_window_length,
            max_test_window_length=self.max_test_window_length
        )
        return time_series_backtest_dataset
