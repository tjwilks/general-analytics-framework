import json


class NodeConfig:

    def __init__(self, type, name, child_configs, iterator_config, other_args=None):
        self.type = type
        self.name = name
        self.children = []
        for child_config in child_configs:
            if child_config["type"] in ["node", "composite"]:
                child = NodeConfig(**child_config)
            elif child_config["type"] == "leaf":
                child = LeafConfig(**child_config)
            else:
                raise ValueError("child 'type' must be 'node' or 'leaf'")
            self.children.append(child)
        self.iterator_config = IteratorConfig(**iterator_config)
        if other_args:
            self.other_args = other_args
        else:
            self.other_args = {}


class LeafConfig:
    def __init__(self, type, name, other_args,  iterator_config=None):
        self.type = type
        self.name = name
        if iterator_config:
            self.iterator_config = IteratorConfig(**iterator_config)
        else:
            self.iterator_config = iterator_config
        self.other_args = other_args


class IteratorConfig:
    def __init__(self, name, args=None):
        self.name = name
        if args:
            self.args = args
        else:
            self.args = {}


class ConfigParser:

    def read_config_file(self, path):
        if path.endswith(".json"):
            config_dict = self.read_json(path)
            return config_dict
        else:
            raise ValueError("path must end with '.json'")

    def read_json(self, path: str) -> dict:
        """
        Load the configuration from a JSON file.

        Parameters:
            path (str): Path to the JSON file.

        Returns:
            dict: Loaded configuration.
        """
        with open(path, 'r') as j:
            config = json.loads(j.read())
        return config


