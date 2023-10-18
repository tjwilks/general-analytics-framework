from abc import ABC, abstractmethod
import pandas as pd
from general_analytics_framwork.data_preparation import data_loaders, \
    data_converters


class AbstractProcess(ABC):

    def __init__(self, children):
        self.children = children

    @abstractmethod
    def run(self, data):
        pass


class SequenceProcess(AbstractProcess):

    def run(self, data=None):
        for child in self.children:
            if data is not None:
                data = child.run(data)
            else:
                data = child.run()
        return data


class ParallelProcess(AbstractProcess):

    def run(self, data=None):
        output = {}
        for child in self.children:
            if data is not None:
                child_output = child.run(data)
            else:
                child_output = child.run()
            output[child] = child_output

        return self.aggregate_results(output)

    def aggregate_results(self, output):
        raise NotImplementedError


class DataLoaderComposite(ParallelProcess):

    def __init__(self, children, joining_columns):
        self.joining_columns = joining_columns
        super().__init__(children=children)

    AVAILABLE_STRATEGIES = {
        "local": data_loaders.LocalDataLoader
    }

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
        "time_series": data_converters.TimeseriesConverter,
        "time_series_backtest": data_converters.TimeseriesBacktestConverter
    }

    def __init__(self, children):
        super().__init__(children=children)


class DataPreparationProcess(SequenceProcess):

    AVAILABLE_STRATEGIES = {
        "data_loader": DataLoaderComposite,
        "data_converter": DataConverterComposite
    }

    def __init__(
            self,
            data_loader: DataLoaderComposite,
            data_converter: DataConverterComposite = None
    ):
        self.data_loader = data_loader
        self.data_converter = data_converter
        children = [data_loader]
        if data_converter:
            children.append(data_converter)
        super().__init__(children=children)

