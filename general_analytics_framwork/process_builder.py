from general_analytics_framwork.config import NodeConfig, LeafConfig
from typing import Union


class ProcessBuilder:

    def build(
            self,
            config: Union[NodeConfig, LeafConfig],
            available_processes
    ):
        process_class = available_processes[config.name]
        if config.type == "node":
            process_children = {
                child.name: self.build(
                    child,
                    process_class.AVAILABLE_STRATEGIES
                ) for child in config.children
            }
            process = process_class(**process_children, **config.additional_args)
        elif config.type == "composite":
            process_children = [
                self.build(
                    child,
                    process_class.AVAILABLE_STRATEGIES
                ) for child in config.children
            ]
            process = process_class(process_children, **config.additional_args)
        elif config.type == "leaf":
            process_class = available_processes[config.name]
            process = process_class(**config.args)
        else:
            raise ValueError("child 'type' must be 'node', 'composite', "
                             "or 'leaf'")
        return process
