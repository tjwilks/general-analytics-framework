from abc import ABC, abstractmethod
from general_analytics_framwork.analytics_processes.process_mediators import BacktestAPM
from general_analytics_framwork.analytics_processes.process_configuration import BacktestAPC


class AbstractAnalyticsProcessFactory(ABC):

    AVAILABLE_STRATEGIES = {}

    def __init__(self, strategy_config):
        self.strategy_config = strategy_config

    @abstractmethod
    def create_analytics_process(self):
        """
        Create and return an instance of an analytics process.
        """
        pass

    def create_strategy(
            self,
            strategy_type_name
    ):
        strategy_config = self.strategy_config[strategy_type_name]
        available_strategies = self.AVAILABLE_STRATEGIES.get(
            strategy_type_name, {}
        )
        strategy_class = available_strategies.get(
            strategy_config.name
        )
        if strategy_class:
            return strategy_class(**strategy_config)
        else:
            raise ValueError(f"Invalid {strategy_type_name} strategy: "
                             f"{strategy_config.name}")


class OptimisationAPF(AbstractAnalyticsProcessFactory):

    @abstractmethod
    def create_analytics_process(self):
        """
        Create and return an instance of an analytics process.
        """
        pass


class InferenceAPF(AbstractAnalyticsProcessFactory):

    @abstractmethod
    def create_analytics_process(self):
        """
        Create and return an instance of an analytics process.
        """
        pass


class BacktestAPF(OptimisationAPF):

    AVAILABLE_STRATEGIES = {}
    MEDIATOR = BacktestAPM

    def __init__(self, strategy_config: BacktestAPC):
        super().__init__(strategy_config)

    def create_analytics_process(self):
        """
        Create and return an instance of an analytics process.
        """
        data_loader = self.create_strategy('data_loader') # strategy creation may not always be this simple/standard. It could be more complex - e.g. preprocessing composition object
        preprocessor = self.create_strategy('preprocessor')
        results_output = self.create_strategy('results_output')
        backtester = self.MEDIATOR(
            data_loader=data_loader,
            preprocessor=preprocessor,
            results_output=results_output
        )
        return backtester


class HypothesisTestingAPF(InferenceAPF):

    def create_analytics_process(self):
        """
        Create and return an instance of an analytics process.
        """
        pass
