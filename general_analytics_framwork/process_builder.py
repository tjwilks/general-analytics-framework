from general_analytics_framwork.config import NodeConfig, LeafConfig
from typing import Union


class ProcessBuilder:

    def build(
            self,
            config: Union[NodeConfig, LeafConfig],
            available_processes,
            available_iterators
    ):
        if config.type == "node":
            process = self.build_node(
                config,
                available_processes,
                available_iterators
            )
        elif config.type == "leaf":
            process = self.build_leaf(
                config,
                available_processes,
                available_iterators
            )
        else:
            raise ValueError("child 'type' must be 'node', 'composite', "
                             "or 'leaf'")
        return process

    def build_node(self, config, available_processes, available_iterators):
        iterator = self.build_iterator(
            iterator_config=config.iterator_config,
            available_iterators=available_iterators
        )
        process_class = available_processes[config.name]
        process_children = []
        for child_config in config.children:
            child_class = process_class.AVAILABLE_STRATEGIES[child_config.name]
            child = self.build(
                child_config,
                process_class.AVAILABLE_STRATEGIES,
                child_class.AVAILABLE_ITERATORS
            )
            process_children.append(child)
        process = process_class(
            process_children,
            iterator,
            **config.other_args
        )
        return process

    def build_leaf(self, config, available_processes, available_iterators):
        process_class = available_processes[config.name]
        if available_iterators:
            iterator = self.build_iterator(
                iterator_config=config.iterator_config,
                available_iterators=available_iterators
            )
            process = process_class(**config.other_args, iterator=iterator)
        else:
            process = process_class(**config.other_args)
        return process

    @staticmethod
    def build_iterator(iterator_config, available_iterators):
        iterator_class = available_iterators[iterator_config.name]
        iterator = iterator_class(**iterator_config.args)
        return iterator
