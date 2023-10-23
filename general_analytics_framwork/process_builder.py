from general_analytics_framwork.config import NodeConfig, LeafConfig
from typing import Union


class ProcessBuilder:

    def build(
            self,
            config: Union[NodeConfig, LeafConfig],
            available_processes
    ):
        if config.type == "node":
            process = self.build_node(
                config,
                available_processes
            )
        elif config.type == "leaf":
            process = self.build_leaf(
                config,
                available_processes
            )
        else:
            raise ValueError("child 'type' must be 'node', 'composite', "
                             "or 'leaf'")
        return process

    def build_node(self, config, available_processes):
        process_class = available_processes[config.name]
        process_children = []
        for child_config in config.children:
            child = self.build(
                child_config,
                process_class.AVAILABLE_STRATEGIES
            )
            process_children.append(child)
        process = process_class(
            process_children,
            **config.other_args
        )
        return process

    @staticmethod
    def build_leaf(config, available_processes):
        process_class = available_processes[config.name]
        process = process_class(**config.other_args)
        return process
