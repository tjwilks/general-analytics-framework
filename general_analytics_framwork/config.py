import json


class NodeConfig:

    def __init__(self, type, name, child_configs, other_args=None):
        self.type = type
        self.name = name
        self.children = []
        for child_config in child_configs:
            if child_config["type"] == "node":
                child = NodeConfig(**child_config)
            elif child_config["type"] == "leaf":
                child = LeafConfig(**child_config)
            else:
                raise ValueError("child 'type' must be 'node' or 'leaf'")
            self.children.append(child)
        if other_args:
            self.other_args = other_args
        else:
            self.other_args = {}


class LeafConfig:
    def __init__(self, type, name, other_args):
        self.type = type
        self.name = name
        self.other_args = other_args


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


