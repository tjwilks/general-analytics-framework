from general_analytics_framwork.processes import DataPreparationProcess
from general_analytics_framwork.process_builder import ProcessBuilder
import sys
from general_analytics_framwork.config import ConfigParser, NodeConfig


AVAILABLE_PROCESSES = {
    "data_preparation": DataPreparationProcess
}


def test_basic_process(config):
    process_builder = ProcessBuilder()
    process = process_builder.build(config, AVAILABLE_PROCESSES)
    data = process.run()
    print(data)


if __name__ == '__main__':
    config_loader = ConfigParser()
    config_file_path = sys.argv[1]
    config_dict = config_loader.read_config_file(config_file_path)
    config = NodeConfig(**config_dict)
    test_basic_process(config)
