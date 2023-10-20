from abc import ABC, abstractmethod


class AbstractComponent(ABC):

    AVAILABLE_STRATEGIES = {}
    AVAILABLE_ITERATORS = None

    def __init__(self, iterator=None):
        self.iterator = iterator

    @abstractmethod
    def run(self, data=None):
        pass


class AbstractNode(AbstractComponent):

    AVAILABLE_ITERATORS = {}

    def __init__(self, children, iterator):
        self.children = children
        super().__init__(iterator=iterator)

    @abstractmethod
    def run(self, data=None):
        pass


class SequenceProcess(AbstractNode):

    def run(self, data=None):
        output = self.iterator.iterate(self, data)
        return output


class ParallelProcess(AbstractNode):

    def run(self, data=None):
        output = self.iterator.iterate(self, data)
        return self.aggregate_results(output)

    def aggregate_results(self, output):
        raise NotImplementedError