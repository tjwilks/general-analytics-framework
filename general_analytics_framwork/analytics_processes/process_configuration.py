from abc import ABC, abstractmethod


class AbstractAnalyticsProcessConfiguration(ABC):

    @abstractmethod
    def load_configuration(self):
        """
        Load the analytics process configuration.
        """
        pass


class OptimisationAPC(AbstractAnalyticsProcessConfiguration):

    @abstractmethod
    def load_configuration(self):
        """
        Load the analytics process configuration.
        """
        pass


class InferenceAPC(AbstractAnalyticsProcessConfiguration):

    @abstractmethod
    def load_configuration(self):
        """
        Load the analytics process configuration.
        """
        pass


class BacktestAPC(OptimisationAPC):

    def load_configuration(self):
        pass


class HypothesisTestingAPC(InferenceAPC):

    def load_configuration(self):
        pass
