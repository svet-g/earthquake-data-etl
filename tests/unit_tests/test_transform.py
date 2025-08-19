import os
import logging
from pathlib import Path
from unittest.mock import patch
import pytest
import pandas as pd
from src.transform.transform import transform

@pytest.fixture
def test_file_path_transformed_data():
    return Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_transformed_data.json'

@pytest.fixture
def columns_to_drop():
    return ['tz',
            'detail',
            'mmi',
            'status',
            'net',
            'code',
            'ids',
            'sources',
            'types',
            'nst',
            'dmin',
            'rms',
            'gap',
            'type',
            'title']

class TestTransform:
    def test_returns_a_dataframe(self, test_data_file_path, test_file_path_transformed_data, columns_to_drop):
        # act
        df = transform(test_data_file_path, test_file_path_transformed_data, columns_to_drop)
        # assert
        assert isinstance(df, pd.DataFrame)
        
    def test_saves_transformed_data_to_a_local_json_file(self, test_data_file_path, test_file_path_transformed_data, columns_to_drop):
        transform(test_data_file_path, test_file_path_transformed_data, columns_to_drop)
        saved_file = os.path.isfile(test_file_path_transformed_data)
        assert saved_file
        if saved_file:
            os.remove(test_file_path_transformed_data)
    
    @patch("src.transform.transform.geopandas.read_file")
    def test_logs_failure_if_Exception_raised(self, mocked_file_read, test_data_file_path, test_file_path_transformed_data, columns_to_drop, caplog):
        with caplog.at_level(logging.ERROR):
            mocked_file_read.side_effect = Exception
            transform(test_data_file_path, test_file_path_transformed_data, columns_to_drop)
            assert "An unexpected error occured:" in caplog.text
    