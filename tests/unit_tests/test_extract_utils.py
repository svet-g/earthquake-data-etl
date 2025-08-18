import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
import json
import logging
from requests import exceptions
import datetime
from src.utils.extract_utils import extract_initial_month, extract_sample


class TestExtractInitialMonth:

    @patch(
        "src.utils.extract_utils.requests.get"
    )  # turn the whole patch and arrage process into a fixture cause reusing - maybe chain several fixtures in conftest so can use just one if needed
    def test_calls_the_API(self, mocked_get, test_geojson):
        # arrange
        file_path_data = (
            Path(__file__).parent.parent.parent
            / "data"
            / "test"
            / "test_extract.geojson"
        )
        file_path_tracker = (
            Path(__file__).parent.parent.parent / "test_extract_tracker.json"
        )
        url = "fake url"
        mocked_get.return_value.json.return_value = test_geojson
        # act
        extract_initial_month(url, file_path_data, file_path_tracker)
        # assert
        mocked_get.assert_called_once_with(url)
        # clean up test file
        os.remove(file_path_data)
        os.remove(file_path_tracker)

    @patch("src.utils.extract_utils.requests.get")
    def test_saves_data_and_tracker_to_specified_file(self, mocked_get, test_geojson):
        # arrange
        mocked_get.return_value.json.return_value = test_geojson
        # act
        file_path_data = (
            Path(__file__).parent.parent.parent
            / "data"
            / "test"
            / "test_extract.geojson"
        )
        file_path_tracker = (
            Path(__file__).parent.parent.parent / "test_extract_tracker.json"
        )
        url = "fake url"
        extract_initial_month(url, file_path_data, file_path_tracker)
        # assert
        assert os.path.isfile(file_path_data)
        assert os.path.isfile(file_path_tracker)
        # clean up test file
        os.remove(file_path_data)
        os.remove(file_path_tracker)

    @patch("src.utils.extract_utils.requests.get")
    def test_logs_success(self, mocked_get, test_geojson, caplog):
        with caplog.at_level(logging.INFO):
            # arrange
            file_path_data = (
                Path(__file__).parent.parent.parent
                / "data"
                / "test"
                / "test_extract.geojson"
            )
            file_path_tracker = (
                Path(__file__).parent.parent.parent / "test_extract_tracker.json"
            )
            url = "fake url"
            mocked_get.return_value.json.return_value = test_geojson
            # act
            extract_initial_month(url, file_path_data, file_path_tracker)
            # assert
            assert (
                "Starting initial data extraction process of first month of earthquake data"
                in caplog.text
            )
            # clean up test file
            os.remove(file_path_data)
            os.remove(file_path_tracker)

    @patch("src.utils.extract_utils.requests.get")
    @patch("src.utils.extract_utils.datetime.datetime")
    def test_returns_poll_time_dict(self, mocked_datetime, mocked_get, test_geojson):
        # arrange
        file_path_data = (
            Path(__file__).parent.parent.parent
            / "data"
            / "test"
            / "test_extract.geojson"
        )
        file_path_tracker = (
            Path(__file__).parent.parent.parent / "test_extract_tracker.json"
        )
        url = "fake url"
        mocked_get.return_value.json.return_value = test_geojson
        mocked_datetime.now.return_value.strftime.return_value = "1993-08-17T10:31:19"
        expected = {"time": "1993-08-17T10:31:19"}
        # act
        actual = extract_initial_month(url, file_path_data, file_path_tracker)
        # assert
        assert expected == actual
        # clean up test file
        os.remove(file_path_data)
        os.remove(file_path_tracker)

    @patch("src.utils.extract_utils.requests.get")
    @patch("src.utils.extract_utils.datetime.datetime")
    def test_logs_tracker_file_creation(
        self, mocked_datetime, mocked_get, test_geojson, caplog
    ):
        with caplog.at_level(logging.INFO):
            # arrange
            file_path_data = (
                Path(__file__).parent.parent.parent
                / "data"
                / "test"
                / "test_extract.geojson"
            )
            file_path_tracker = (
                Path(__file__).parent.parent.parent / "test_extract_tracker.json"
            )
            url = "fake url"
            mocked_get.return_value.json.return_value = test_geojson
            mocked_datetime.now.return_value.strftime.return_value = (
                "1993-08-17T10:31:19"
            )
            # act
            extract_initial_month(url, file_path_data, file_path_tracker)
            # assert
            assert (
                "Tracker file successful created - time: 1993-08-17T10:31:19, path: /home/svet-g/df/capstone/earthquake-data-etl/test_extract_tracker.json"
                in caplog.text
            )
            # clean up test file
            os.remove(file_path_data)
            os.remove(file_path_tracker)

    # can also test that the json file contains the right time and is in the right format

class TestExtractSample:
    
    def test_returns_10_rows_of_data_from_original_data(self, test_data_file_path):
        # arrange
        file_path_read = (
        Path(__file__).parent.parent.parent
        / 'data'
        / 'test'
        / 'test_earthquake_data_last_30_days_full.geojson'
        )
        expected_length = 10
        expected_keys =  ['type', 'metadata', 'features', 'bbox']
        # act
        actual = extract_sample(file_path_read, test_data_file_path)
        actual_length = len(actual['features'])
        actual_keys = [key for key in actual.keys()]
        # check the full structure - the keys inside the keys
        # check types correspond to original
        # check it duplicates the rows
        # do not check any specific values as that would not work when I poll the API
        # assert
        assert expected_length == actual_length
        assert expected_keys == actual_keys
    
    def test_creates_sample_json_file(self, test_data_file_path):
        # arrange
        file_path_read = (
        Path(__file__).parent.parent.parent
        / 'data'
        / 'test'
        / 'test_earthquake_data_last_30_days_full.geojson'
        )
        # act
        extract_sample(file_path_read, test_data_file_path)
        # assert
        assert os.path.isfile(test_data_file_path)
    