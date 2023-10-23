from abc import ABC, abstractmethod


class AbstractComponent(ABC):

    AVAILABLE_STRATEGIES = {}

    @abstractmethod
    def run(self, data=None):
        pass


class AbstractNode(AbstractComponent):

    def __init__(self, children):
        self.children = children

    @abstractmethod
    def run(self, data=None):
        pass

    @abstractmethod
    def iterate(self, process, data):
        pass


class SequenceProcess(AbstractNode):

    def run(self, data=None):
        output = self.iterate(self, data)
        return output

    def iterate(self, process, data=None):
        for child in process.children:
            if data is not None:
                data = child.run(data)
            else:
                data = child.run()
        return data


class ParallelAggregateProcess(AbstractNode):

    def run(self, data=None):
        output = self.iterate(self, data)
        return self.aggregate_results(output)

    def iterate(self, process, data=None):
        output = {}
        for child in process.children:
            if data is not None:
                child_output = child.run(data)
            else:
                child_output = child.run()
            output[child] = child_output

        return output

    def aggregate_results(self, output):
        raise NotImplementedError


class DataAggregationSequenceProcess(AbstractNode):

    def run(self, data):
        output = self.iterate(self.execution_process, data)
        return output

    def iterate(self, process, data):
        output = []
        for element in data:
            element_output = process(element)
            output.append(element_output)
        return output