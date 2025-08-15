import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
import json
import logging
from requests import exceptions
from src.utils.extract_utils import extract_initial_month

class TestExtractInitialMonth():
    
    @patch('src.utils.extract_utils.requests.get') # turn the whole patch and arrage process into a fixture cause reusing - maybe chain several fixtures in conftest so can use just one if needed
    def test_calls_the_API(self, mocked_get, mocked_geojson):
        # arrange
        file_path = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
        url = 'fake url'
        mocked_get.return_value.json.return_value = mocked_geojson
        # act
        extract_initial_month(url, file_path)
        # assert
        mocked_get.assert_called_once_with(url)
        # clean up test file
        os.remove(file_path)
    
    @patch('src.utils.extract_utils.requests.get')
    def test_saves_data_to_specified_file(self, mocked_get, mocked_geojson):
        # arrange
        mocked_get.return_value.json.return_value = mocked_geojson
        # act
        file_path = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
        url = 'fake url'
        extract_initial_month(url, file_path)
        # assert
        assert os.path.isfile(file_path)
        # clean up test file
        os.remove(file_path)
        
    @patch('src.utils.extract_utils.requests.get')
    def test_logs_success(self, mocked_get, mocked_geojson, caplog):
        with caplog.at_level(logging.INFO):
            # arrange
            file_path = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
            url = 'fake url'
            mocked_get.return_value.json.return_value = mocked_geojson
            # act
            extract_initial_month(url, file_path)
            # assert
            assert 'Starting initial data extraction process of first month of earthquake data' in caplog.text
            # clean up test file
            os.remove(file_path)
    
    def test_logs_failure_if_RequestException_raised(self, caplog):
        with caplog.at_level(logging.ERROR):
            # arrange
            file_path = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
            url = 'fake url'
            # act
            extract_initial_month(url, file_path)
            # assert
            assert 'A RequestException occured:' in caplog.text
    
    @patch('src.utils.extract_utils.requests.get')
    def test_logs_failure_if_HTTPError_raised(self, mocked_get, caplog):
        with caplog.at_level(logging.ERROR):
            # arrange
            file_path = Path(__file__).parent.parent.parent / 'data' / 'test' / 'test_extract.geojson'
            url = 'fake url'
            mocked_get.side_effect = exceptions.HTTPError
            # act
            extract_initial_month(url, file_path)
            # assert
            assert 'An HTTPError occured' in caplog.text