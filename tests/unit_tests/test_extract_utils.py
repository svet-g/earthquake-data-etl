import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
import json
import logging
from requests import exceptions
import datetime
from src.utils.extract_utils import extract_initial_month

class TestExtractInitialMonth():
    
    @patch('src.utils.extract_utils.requests.get') # turn the whole patch and arrage process into a fixture cause reusing - maybe chain several fixtures in conftest so can use just one if needed
    def test_calls_the_API(self, mocked_get, mocked_geojson):
        # arrange
        file_path_data = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
        file_path_tracker = Path(__file__).parent.parent.parent / 'test_extract_tracker.json'
        url = 'fake url'
        mocked_get.return_value.json.return_value = mocked_geojson
        # act
        extract_initial_month(url, file_path_data, file_path_tracker)
        # assert
        mocked_get.assert_called_once_with(url)
        # clean up test file
        os.remove(file_path_data)
        os.remove(file_path_tracker)
    
    @patch('src.utils.extract_utils.requests.get')
    def test_saves_data_and_tracker_to_specified_file(self, mocked_get, mocked_geojson):
        # arrange
        mocked_get.return_value.json.return_value = mocked_geojson
        # act
        file_path_data = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
        file_path_tracker = Path(__file__).parent.parent.parent / 'test_extract_tracker.json'
        url = 'fake url'
        extract_initial_month(url, file_path_data, file_path_tracker)
        # assert
        assert os.path.isfile(file_path_data)
        assert os.path.isfile(file_path_tracker)
        # clean up test file
        os.remove(file_path_data)
        os.remove(file_path_tracker)
        
    @patch('src.utils.extract_utils.requests.get')
    def test_logs_success(self, mocked_get, mocked_geojson, caplog):
        with caplog.at_level(logging.INFO):
            # arrange
            file_path_data = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
            file_path_tracker = Path(__file__).parent.parent.parent / 'test_extract_tracker.json'
            url = 'fake url'
            mocked_get.return_value.json.return_value = mocked_geojson
            # act
            extract_initial_month(url, file_path_data, file_path_tracker)
            # assert
            assert 'Starting initial data extraction process of first month of earthquake data' in caplog.text
            # clean up test file
            os.remove(file_path_data)
            os.remove(file_path_tracker)
            
    @patch('src.utils.extract_utils.requests.get')
    @patch('src.utils.extract_utils.datetime.datetime')
    def test_returns_poll_time_dict(self, mocked_datetime, mocked_get, mocked_geojson):
        # arrange
        file_path_data = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
        file_path_tracker = Path(__file__).parent.parent.parent / 'test_extract_tracker.json'
        url = 'fake url'
        mocked_get.return_value.json.return_value = mocked_geojson
        mocked_datetime.now.return_value.strftime.return_value = '1993-08-17T10:31:19'
        expected = {'time': '1993-08-17T10:31:19'}
        # act
        actual = extract_initial_month(url, file_path_data, file_path_tracker)
        # assert
        assert expected == actual
        # clean up test file
        os.remove(file_path_data)
        os.remove(file_path_tracker)
    
    # can also test that the json file contains the right time and is in the right format