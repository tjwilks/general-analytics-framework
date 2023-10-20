from abc import ABC, abstractmethod


class AbstractIterator(ABC):

    @abstractmethod
    def iterate(self, process, data):
        pass


class SequenceIterator(AbstractIterator):

    def iterate(self, process, data=None):
        for child in process.children:
            if data is not None:
                data = child.run(data)
            else:
                data = child.run()
        return data


class ParallelAggregationIterator(AbstractIterator):

    def iterate(self, process, data=None):
        output = {}
        for child in process.children:
            if data is not None:
                child_output = child.run(data)
            else:
                child_output = child.run()
            output[child] = child_output

        return output


class ParallelIterator(AbstractIterator):

    def iterate(self, process, data):
        for child in process.children:
            child.run(data)


class DataAggregationSequenceIterator(AbstractIterator):

    def iterate(self, process, data=None):
        output = []
        for element in data:
            element_output = process(element)
            output.append(element_output)
        return output


class DataframeAggregationSequenceIterator(AbstractIterator):

    def __init__(self, series_id_col):
        self.series_id_col = series_id_col

    def iterate(self, process, data):
        output = []
        for series_id in data[self.series_id_col].unique():
            element = data[data[self.series_id_col] == series_id]
            output_element = process(series_id, element)
            output.append(output_element)
        return output


class DataSequenceIterator(AbstractIterator):

    def iterate(self, process, data):
        for element in data:
            process(element)
