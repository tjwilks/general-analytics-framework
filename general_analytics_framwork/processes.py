import pandas as pd
from general_analytics_framwork.base_processes import (
    SequenceProcess,
    ParallelProcess
)
from general_analytics_framwork.data_preparation.data_loaders import (
    LocalDataLoader
)
from general_analytics_framwork.data_preparation.data_converters import (
    TimeseriesConverter, TimeseriesBacktestConverter
)

from general_analytics_framwork.modelling import (
    RandomWalk,
    ARIMA
)

from general_analytics_framwork.visualisation import (
    TimeseriesPlotter,
    BarGraphPlotter,
    AutocorrelationPlotter,
    ForecastGraphPlotter
)


class DataLoaderComposite(SequenceProcess):

    AVAILABLE_STRATEGIES = {
        "local": LocalDataLoader
    }

    def __init__(self, children, joining_columns):
        self.joining_columns = joining_columns
        super().__init__(children=children)

    def run(self, data=None):
        output = None
        for child in self.children:
            if data is not None:
                child_output = child.run(data)
            else:
                child_output = child.run()
            output = self.aggregate_results(output, child_output)
        return output

    def aggregate_results(self, output, child_output):
        if output is None:
            result = child_output
        else:
            result = pd.merge(
                left=output,
                right=child_output,
                on=self.joining_columns,
                how='inner'
            )
        return result


class DataConverterComposite(SequenceProcess):

    AVAILABLE_STRATEGIES = {
        "time_series": TimeseriesConverter,
        "time_series_backtest": TimeseriesBacktestConverter
    }


class DataPreparationProcess(SequenceProcess):

    AVAILABLE_STRATEGIES = {
        "data_loader": DataLoaderComposite,
        "data_converter": DataConverterComposite
    }

    def __init__(self, children):
        assert type(children[0]) == DataLoaderComposite, \
            "first child process of DataPreparation must be a " \
            "DataLoaderComposite"

        super().__init__(children=children)


class ModellingProcess(SequenceProcess):
    AVAILABLE_STRATEGIES = {
        "random_walk": RandomWalk,
        "arima": ARIMA
    }


class DataVisualisationProcess(ParallelProcess):
    AVAILABLE_STRATEGIES = {
        "time_series": TimeseriesPlotter,
        "bar_graph": BarGraphPlotter,
        "auto_correlation": AutocorrelationPlotter
    }


class ForecastDataVisualisationProcess(ParallelProcess):
    AVAILABLE_STRATEGIES = {
        "forecast_plot": ForecastGraphPlotter
    }


class DataPresentationProcess(SequenceProcess):
    AVAILABLE_STRATEGIES = {
        "data_preparation": DataPreparationProcess,
        "data_visualisation": DataVisualisationProcess
    }


class ModelExperimentationProcess(SequenceProcess):
    AVAILABLE_STRATEGIES = {
        "data_preparation": DataPreparationProcess,
        "modelling": ModellingProcess,
        "forecast_data_visualisation": ForecastDataVisualisationProcess
    }
