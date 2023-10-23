from abc import ABC, abstractmethod


class AbstractComponent(ABC):

    AVAILABLE_STRATEGIES = {}

    @abstractmethod
    def run(self, data):
        pass


class AbstractNode(AbstractComponent):

    def __init__(self, children):
        self.children = children

    @abstractmethod
    def run(self, data):
        pass


class SequenceProcess(AbstractNode):

    def run(self, data=None):
        for child in self.children:
            if data is not None:
                data = child.run(data)
            else:
                data = child.run()
        return data


class ParallelProcess(AbstractNode):

    def run(self, data):
        for child in self.children:
            child.run(data)
