from abc import ABC, abstractmethod
import pandas as pd
import os
from general_analytics_framwork.base_processes import AbstractComponent


class LocalDataLoader(AbstractComponent):
    """
    DataLoader class to load data from different sources.

    Methods:
        load(source_type: str, path: str) -> pd.DataFrame:
            Load data from a source based on source type.

    """

    def __init__(self, source_type, path):
        self.source_type = source_type
        self.path = path

    def run(self) -> pd.DataFrame:
        """
        Load data from a source based on source type.

        Parameters:
            source_type (str): Type of data source ('dir' or 'csv').
            path (str): Path to the data source.

        Returns:
            pd.DataFrame: Loaded data.
        """
        if self.source_type == 'dir':
            data = self.load_from_dir(self.path)
        elif self.source_type == 'csv':
            data = self.load_from_csv(self.path)
        else:
            raise ValueError("DataLoader load method's source_type argument "
                             "must be either 'dir' or 'csv'")
        return data

    def load_from_dir(self, path: str) -> pd.DataFrame:
        """
        Load data from multiple CSV files in a directory.

        Parameters:
            path (str): Path to the directory.

        Returns:
            pd.DataFrame: Concatenated dataset from CSV files.
        """
        filenames = [
            os.path.join(path, f) for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ]
        datasets = []
        for file in filenames:
            data = self.load_from_csv(file)
            datasets.append(data)
        return pd.concat(datasets, axis=0)

    def load_from_csv(self, path: str) -> pd.DataFrame:
        """
        Load forex data from a CSV file.

        Parameters:
            path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded forex data.
        """
        data = pd.read_csv(
            path
        )
        return data


class ForexLoader(LocalDataLoader):
    """
    ForexLoader class to load forex data.

    Methods:
        load_from_csv(path: str) -> pd.DataFrame:
            Load forex data from a CSV file.

    """

    def load_from_csv(self, path: str) -> pd.DataFrame:
        """
        Load forex data from a CSV file.

        Parameters:
            path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded forex data.
        """
        data = pd.read_csv(
            path,
            parse_dates=['Date'],
            date_format="%Y-%m-%d"
        )
        data = data.rename(columns={"Date": "date"})
        data = data.set_index("date").resample('W').mean().reset_index()
        data['currency_pair'] = f"USD/{os.path.basename(path)[:3]}"
        return data