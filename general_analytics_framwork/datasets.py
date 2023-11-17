from typing import List, Union, Dict
from datetime import datetime
import numpy as np
from sklearn import metrics


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
                 train_window_length: int,
                 max_test_window_length: int
                 ) -> None:
        """
        Initializes a new instance of the BacktestWindow class.

        :param n_obs: The total number of observations in the time series.
        :param train_window_len: The length of the training window.
        :param max_test_window_length: The maximum length of the test window.

        """

        self.n_obs = n_obs
        self.train_window_length = train_window_length
        self.max_test_window_length = max_test_window_length
        max_time_series_index = self.n_obs - 1
        max_requested_time_series_index = self.train_window_length
        assert max_time_series_index >= max_requested_time_series_index, \
            "time series is too short to initialise window with requested " \
            "train_window_length"
        self.test_end_index = self.n_obs - 1
        self.test_start_index = self.n_obs - 1
        self.train_end_index = self.n_obs - 2
        self.train_start_index = self.n_obs - 1 - self.train_window_length
        self.test_window_length = 1
        self.index = 0

    def move(self, move_amount):
        """
        Move the window to the next position in the time series.

        :raises AssertionError: If the start index of the training window is
        less than 0.
        """
        self.train_start_index += move_amount
        self.train_end_index += move_amount
        self.test_end_index += move_amount
        self.test_start_index += move_amount
        self.test_window_length = self.test_end_index - self.test_start_index + 1
        self.index -= move_amount

    def move_to_index(self, window_index):
        self.move(self.index-window_index)

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
                 max_test_window_length, predictions=None):
        self.time_series_dataset = time_series_dataset
        self.window = BacktestWindow(
            n_obs=len(time_series_dataset.dates),
            train_window_length=train_window_length,
            max_test_window_length=max_test_window_length
        )
        if predictions:
            self.predictions = predictions
        else:
            self.predictions = {}

    def add_prediction(self, model, prediction):
        if model.get_reference() not in self.predictions.keys():
            self.predictions[model.get_reference()] = {}
        self.predictions[model.get_reference()][self.window.index] = {
            "prediction": prediction,
            "model": model
        }

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

    def get_data(self, requested_data, train_or_test, window_index=None):
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
        if window_index:
            current_window_index = self.window.index
            self.window.move_to_index(window_index=window_index)
        start_index, end_index = self._get_start_and_end_index(train_or_test)
        if requested_data == "y":
            data = self.time_series_dataset.y_data[start_index: end_index+1]
        elif requested_data == "dates":
            data = self.time_series_dataset.dates[start_index: end_index+1]
        elif requested_data == "regressors":
            if self.time_series_dataset.regressor_data:
                data = {regressor_name: regressor[start_index: end_index+1]
                        for regressor_name, regressor
                        in self.time_series_dataset.regressor_data.items()}
            else:
                data = None
        else:
            raise ValueError("requested_data must be 'y', 'dates' "
                             "or regressors")
        if window_index:
            self.window.move_to_index(current_window_index)
        return data

    def __iter__(self):
        return self

    def __next__(self):
        """
        Move the backtest window to the next position in the time series.
        """
        if self.window.train_start_index == 0:
            self.window.move_to_index(0)
            raise StopIteration
        else:
            self.window.move(-1)
            return self


class TimeSeriesBacktestResultsDataset:

    def __init__(
            self,
            backtest_dataset: TimeseriesBacktestDataset
    ):
        self.backtest_dataset = backtest_dataset

    def get_model_error(
            self,
            error_averaging_function,
            error_function,
            model_references=None
    ):
        model_error = {}
        if not model_references:
            model_references = self.backtest_dataset.predictions.keys()

        for model_reference in model_references:
            all_window_model_error = self.get_all_window_model_error(
                model_reference,
                error_function
            )
            error_array = list(all_window_model_error.values())
            model_error[model_reference] = error_averaging_function(
                error_array
            )

        return model_error

    def get_all_window_model_error(self, model_reference, error_function):
        model_predictions = self.backtest_dataset.predictions[model_reference]
        all_window_model_error = {}
        for window_index, prediction_data in model_predictions.items():
            first_date_of_forecast = self.backtest_dataset.get_data(
                "dates",
                "test",
                window_index
            )[0]
            all_window_model_error[first_date_of_forecast] = error_function(
                np.array(prediction_data['prediction']),
                np.array(self.backtest_dataset.get_data("y", "test", window_index))
            )
        return all_window_model_error

    def get_single_window_model_error(self, model_reference, window):
        all_window_model_error = self.get_all_window_model_error(
            model_reference
        )
        single_window_model_error = all_window_model_error[window]
        return single_window_model_error


class WindowPredictionDataset:

    AVAILABLE_ERROR_FUNCTIONS = {
        "MSE": metrics.mean_squared_error,
        "MAE": metrics.mean_absolute_error
    }

    def __init__(self, window_prediction_data, error_function):
        self.model_data = {
            data["model"]:
            {"prediction": data['prediction'], 'y_test': data['y_test']}
            for data in window_prediction_data
        }
        self.error_function = self.AVAILABLE_ERROR_FUNCTIONS[error_function]

    def calculate_model_error(self):
        model_error = {
            data["model"]: self.error_function(
                data['prediction'],
                data['y_test']
            )
            for data in self.model_data
        }
        return model_error
