from abc import ABC, abstractmethod


class AbstractAnalyticsProcessMediator(ABC):

    @abstractmethod
    def run_process(self):
        """
        Run the analytics process.
        """
        pass


class OptimisationAPM(AbstractAnalyticsProcessMediator):

    @abstractmethod
    def run_process(self):
        """
        Run the analytics process.
        """
        pass


class InferenceAPM(AbstractAnalyticsProcessMediator):

    @abstractmethod
    def run_process(self):
        """
        Run the analytics process.
        """
        pass


class BacktestAPM(OptimisationAPM):

    def __init__(self, data_loader, preprocessor, results_output):
        self.data_loader = data_loader
        self.preprocessor = preprocessor
        self.results_output = results_output

    def run_process(self):
        pass


class HypothesisTestingAPF(InferenceAPM):

    def run_process(self):
        pass
