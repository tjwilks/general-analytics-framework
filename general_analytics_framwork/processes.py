import pandas as pd
from general_analytics_framwork.base_processes import (
    ParallelAggregateProcess,
    SequenceProcess
)
from general_analytics_framwork.data_preparation.data_loaders import (
    LocalDataLoader
)
from general_analytics_framwork.data_preparation.data_converters import (
    TimeseriesConverter, TimeseriesBacktestConverter
)
from general_analytics_framwork.iterators import (
    SequenceIterator, DataSequenceIterator
)
from general_analytics_framwork.visualisation import (
    DataVisualisationProcess
)


class DataLoaderComposite(ParallelAggregateProcess):

    AVAILABLE_STRATEGIES = {
        "local": LocalDataLoader
    }

    def __init__(self, children, iterator, joining_columns):
        self.joining_columns = joining_columns
        super().__init__(children=children, iterator=iterator)

    def aggregate_results(self, output):
        result = None
        for child, dataset in output.items():
            if result is None:
                result = dataset
            else:
                result = pd.merge(
                    left=result,
                    right=dataset,
                    on=self.joining_columns,
                    how='inner'
                )
        return result


class DataConverterComposite(SequenceProcess):

    AVAILABLE_STRATEGIES = {
        "time_series": TimeseriesConverter,
        "time_series_backtest": TimeseriesBacktestConverter
    }
    AVAILABLE_ITERATORS = {
        "sequence": SequenceIterator,
        "data_sequence": DataSequenceIterator
    }


class DataPreparationProcess(SequenceProcess):

    AVAILABLE_STRATEGIES = {
        "data_loader": DataLoaderComposite,
        "data_converter": DataConverterComposite
    }

    def __init__(self, children, iterator):
        assert type(children[0]) == DataLoaderComposite, \
            "first child process of DataPreparation must be a " \
            "DataLoaderComposite"

        super().__init__(children=children, iterator=iterator)


class DataPresentationProcess(SequenceProcess):
    AVAILABLE_STRATEGIES = {
        "data_preparation": DataPreparationProcess,
        "data_visualisation": DataVisualisationProcess
    }
