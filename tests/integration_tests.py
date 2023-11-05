from general_analytics_framwork.processes import DataPreparationProcess, ModelExperimentationProcess, DataPresentationProcess
from general_analytics_framwork.process_builder import ProcessBuilder
from general_analytics_framwork.config import ConfigParser, NodeConfig


AVAILABLE_PROCESSES = {
    "data_presentation": DataPresentationProcess,
    "model_experimentation": ModelExperimentationProcess
}


def test_process(config_file_path):
    config_loader = ConfigParser()
    config_dict = config_loader.read_config_file(config_file_path)
    config = NodeConfig(**config_dict)
    process_builder = ProcessBuilder()
    process = process_builder.build(
        config,
        AVAILABLE_PROCESSES
    )
    output = process.run()
    return output


if __name__ == '__main__':
    output = test_process("config/modelling.json")
    print(output)
    test_process("config/data_presentation.json")
