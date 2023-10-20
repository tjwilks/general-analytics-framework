from typing import List, Union, Dict
from datetime import datetime


class TimeseriesDataset:

    def __init__(
            self,
            series_id: str,
            dates: List[datetime.date],
            y_data: List[Union[float, int]],
            regressor_data: Dict[str, List[Union[float, int]]] = None,
            date_parser: str = None
    ):
        assert len(dates) == len(y_data), f"dates and y_data parameters must " \
                                          f"be of same length." \
                                          f"\ndates length:" f"{len(dates)} " \
                                          f"\ny_data length {len(y_data)}"
        self.series_id = series_id
        if date_parser:
            self.dates = [
                datetime.strptime(date, date_parser) for date in dates
            ]
        else:
            self.dates = dates
        assert all([type(date) == datetime for date in self.dates]), \
            "dates are not of type datetime. Either convert the 'dates'" \
            "argument prior initialisation or provide 'date_parser' to convert"

        self.y_data = y_data
        self.regressor_data = regressor_data


class BacktestWindow:
    """
     A class representing a sliding window for backtesting time series data.

    This class defines a sliding window over a time series dataset for use in
    backtesting. The window's training and test periods slide through the data,
    allowing for the evaluation of forecasting models over different time intervals.
    """
    def __init__(self,
                 n_obs: int,
                 train_window_len: int,
                 max_test_window_length: int
                 ) -> None:
        """
        Initializes a new instance of the BacktestWindow class.

        :param n_obs: The total number of observations in the time series.
        :param train_window_len: The length of the training window.
        :param max_test_window_length: The maximum length of the test window.

        """
        max_time_series_index = n_obs - 1
        max_requested_time_series_index = train_window_len
        assert max_time_series_index >= max_requested_time_series_index, \
            "time series is too short to initialise window with requested " \
            "train_window_length"
        self.test_end_index = n_obs - 1
        self.test_start_index = n_obs - 1
        self.train_end_index = n_obs - 2
        self.train_start_index = n_obs - 1 - train_window_len
        self.test_window_length = 1
        self.max_test_window_length = max_test_window_length
        self.index = 0

    def is_not_last(self):
        """
        Check if the current window is not the last window in the time series.

        :return: True if the current window is not the last; otherwise, False.
        """
        return self.train_start_index != 0

    def next(self):
        """
        Move the window to the next position in the time series.

        :raises AssertionError: If the start index of the training window is
        less than 0.
        """
        assert self.is_not_last(), "Start index of training window can not " \
                                   "be less than 0"
        self.train_start_index -= 1
        self.train_end_index -= 1
        if self.test_window_length == self.max_test_window_length:
            self.test_end_index -= 1
        self.test_start_index -= 1
        self.test_window_length = self.test_end_index - self.test_start_index + 1
        self.index += 1

    def get_train_index(self):
        """
        Get the start and end indices of the training window.

        :return: A tuple of the start and end indices of the training window.
        """
        return self.train_start_index, self.train_end_index

    def get_test_index(self):
        """
        Get the start and end indices of the test window.

        :return: A tuple of the start and end indices of the test window.
        """
        return self.test_start_index, self.test_end_index


class TimeseriesBacktestDataset:

    def __init__(self, time_series_dataset, train_window_length,
                 max_test_window_length):
        self.time_series_dataset = time_series_dataset
        self.window = BacktestWindow(
            n_obs=len(time_series_dataset.dates),
            train_window_len=train_window_length,
            max_test_window_length=max_test_window_length
        )

    def _get_start_and_end_index(self, train_or_test):
        """
        Get the start and end indices of the training or test window.

        :param train_or_test: Either "train" or "test" to specify the window
        type.
        :return: A tuple of the start and end indices of the window.
        :raises ValueError: If an invalid value for train_or_test is provided.
        """
        if train_or_test == "train":
            return self.window.get_train_index()
        elif train_or_test == "test":
            return self.window.get_test_index()
        else:
            raise ValueError("train_or_test must be either 'train' or 'test'")

    def get_data(self, requested_data, train_or_test):
        """
        Get the requested data (target values, dates, or regressors) for the
        specified window.

        :param requested_data: The type of data to retrieve ("y", "dates", or
         "regressors").
        :param train_or_test: Either "train" or "test" to specify the window
        type.
        :return: The requested data for the specified window.
        :raises ValueError: If an invalid value for requested_data or
        train_or_test is provided.
        """
        start_index, end_index = self._get_start_and_end_index(train_or_test)
        if requested_data == "y":
            return self.time_series_dataset.y_data[start_index: end_index+1]
        elif requested_data == "dates":
            return self.time_series_dataset.dates[start_index: end_index+1]
        elif requested_data == "regressors":
            if self.time_series_dataset.regressor_data:
                return {regressor_name: regressor[start_index: end_index+1]
                        for regressor_name, regressor
                        in self.time_series_dataset.regressor_data.items()}
            else:
                return None
        else:
            raise ValueError("requested_data must be 'y', 'dates' "
                             "or regressors")

    def get_data_for_forecast(self):
        """
        Get the data required for forecasting for the current window.

        :return: A dictionary containing the data required for forecasting.
        """
        data_for_forecast = {
            "series_id": self.time_series_dataset.series_id,
            "y_train": self.get_data("y", "train"),
            "y_test": self.get_data("y", "test"),
            "dates_train": self.get_data("dates", "train"),
            "dates_test": self.get_data("dates", "test"),
            "regressors_train": self.get_data("regressors", 'train'),
            "regressors_test": self.get_data("regressors", 'test'),
            "window_index": self.window.index
         }
        return data_for_forecast

    def next_window(self):
        """
        Move the backtest window to the next position in the time series.
        """
        self.window.next()
