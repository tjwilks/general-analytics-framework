from abc import abstractmethod, ABC
from typing import List, Optional, Dict, Union
from statsmodels.tsa.statespace.sarimax import SARIMAX
from general_analytics_framwork.base_processes import AbstractComponent
from general_analytics_framwork.datasets import TimeseriesBacktestDataset


class TimeSeriesModel(AbstractComponent):

    def run(self, data):
        for backtest_dataset in data:
            for window in backtest_dataset:
                self.fit_predict(window)
        return data

    def fit_predict(self, data: TimeseriesBacktestDataset):
        self.fit(data.get_data("y", "train"), data.get_data("regressors", "train"))
        prediction = self.predict(data.window.test_window_length)
        data.add_prediction(self, data.window.index, prediction)
        return data

    @abstractmethod
    def get_reference(self) -> str:
        """
        Get a reference string for the model.

        Returns:
            str: The reference string.
        """
        raise NotImplementedError

    @abstractmethod
    def fit(
            self,
            y_train: List[float],
            regressors_train: Optional[Dict[str, List[Union[float, int]]]]
    ) -> None:
        """
        Fit the model to the training data.

        Parameters:
            y_train (List[float]): The target values for training.
            regressors_train: Optional[Dict[str, List[Union[float, int]]]]:
                The regressor data
        """
        raise NotImplementedError

    @abstractmethod
    def predict(self, horizon: int) -> List[float]:
        """
        Make predictions for the given horizon.

        Parameters:
            horizon (int): The number of time steps to predict.

        Returns:
            List[float]: The predicted values.
        """
        raise NotImplementedError


class RandomWalk(TimeSeriesModel):
    """
    RandomWalk class representing the Random Walk model.

    Attributes:
        last_observation_seen (Optional[float]): The last observation seen.

    """

    def __init__(self):
        """
        Initialize the Random Walk model.
        """
        self.last_observation_seen: Optional[float] = None
        self._accepts_regressors: bool = False

    def fit(
        self,
        y_train: List[float],
        regressors_train: Optional[Dict[str, List[Union[float, int]]]] = None
    ) -> None:
        """
        Fit the Random Walk model.

        Parameters:
            y_train (List[float]): The target values for training.
            regressors_train (Optional[Dict[str, List[Union[float, int]]]]):
            The regressor data.
        """
        self.last_observation_seen = y_train[-1]

    def predict(self, horizon: int) -> List[float]:
        """
        Make predictions using the Random Walk model.

        Parameters:
            horizon (int): The number of time steps to predict.

        Returns:
            List[float]: The predicted values.
        """
        return [self.last_observation_seen for _ in range(horizon)]

    def get_reference(self) -> str:
        """
        Get a reference string for the Random Walk model.

        Returns:
            str: The reference string.
        """
        return "RandomWalk"


class ARIMA(TimeSeriesModel):
    """
    ARIMA class representing the AutoRegressive Integrated Moving Average model.

    Parameters:
        auto_regressive (int, optional): The number of auto-regressive terms.
        integrated (int, optional): The order of differencing.
        moving_average (int, optional): The number of moving average terms.
        trend_type (str, optional): Type of trend component.

    Attributes:
        order (tuple): Order of ARIMA model.
        trend_type (str): Type of trend component.
        model (SARIMAX): The SARIMAX model instance.

    """

    def __init__(
            self,
            auto_regressive: int = 1,
            integrated: int = 0,
            moving_average: int = 0,
            trend_type: Optional[str] = None):

        """
        Initialize the ARIMA model.

        Parameters:
            auto_regressive (int, optional): The number of auto-regressive terms.
            integrated (int, optional): The order of differencing.
            moving_average (int, optional): The number of moving average terms.
            trend_type (str, optional): Type of trend component.
        """
        self.order = (auto_regressive, integrated, moving_average)
        self.trend_type = trend_type
        self.model: Optional[SARIMAX] = None
        self._accepts_regressors: bool = False

    def fit(
        self,
        y_train: List[float],
        regressors_train: Optional[Dict[str, List[Union[float, int]]]] = None
    ) -> None:
        """
        Fit the ARIMA model.

        Parameters:
            y_train (List[float]): The target values.
            regressors_train (Dict[str, List[Union[float, int]]], optional):
            The regressor data.

        Returns:
            None
        """
        self.model = SARIMAX(
            endog=y_train,
            order=self.order,
            trend=self.trend_type,
            enforce_invertibility=False,
            enforce_stationarity=False
        ).fit(disp=0)

    def predict(self, horizon: int) -> List[float]:
        """
        Make predictions using the ARIMA model.

        Parameters:
            horizon (int): The number of time steps to predict.

        Returns:
            List[float]: The predicted values.
        """
        return self.model.forecast(horizon)

    def get_reference(self) -> str:
        """
        Get a reference string for the ARIMA model.

        Returns:
            str: The reference string.
        """
        reference = f"ARIMA (AR: {self.order[0]}, " \
                    f"I: {self.order[1]}, " \
                    f"MA: {self.order[2]})"
        return reference

