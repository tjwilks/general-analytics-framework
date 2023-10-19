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


class ParallelIterator(AbstractIterator):

    def iterate(self, process, data=None):
        output = {}
        for child in process.children:
            if data is not None:
                child_output = child.run(data)
            else:
                child_output = child.run()
            output[child] = child_output

        return output


