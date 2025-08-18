import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
import json
import logging
from requests import exceptions
from src.extract.extract import extract


class TestExtract:

    @patch("src.extract.extract.extract_initial_month")
    def test_calls_extract_initial_month(self, mocked_extract_intial_month, test_data_file_path):
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
        # act
        extract(url, file_path_data, file_path_tracker, test_data_file_path)
        # assert
        mocked_extract_intial_month.assert_called_once_with(
            url, file_path_data, file_path_tracker
        )

    @patch("src.extract.extract.os.path.isfile")
    def test_logs_failure_if_JSONDecodeError_raised(self, mocked_file_check, test_data_file_path, caplog):
        with caplog.at_level(logging.ERROR):
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
            mocked_file_check.side_effect = exceptions.JSONDecodeError("msg", "doc", 1)
            # act
            extract(url, file_path_data, file_path_tracker, test_data_file_path)
            # assert
            assert "A JSONDecodeError occured" in caplog.text

    @patch("src.extract.extract.os.path.isfile")
    def test_logs_failure_if_HTTPError_raised(self, mocked_file_check, test_data_file_path, caplog):
        with caplog.at_level(logging.ERROR):
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
            mocked_file_check.side_effect = exceptions.HTTPError
            # act
            extract(url, file_path_data, file_path_tracker, test_data_file_path)
            # assert
            assert "An HTTPError occured" in caplog.text

    @patch("src.extract.extract.os.path.isfile")
    def test_logs_failure_if_RequestException_raised(self, mocked_file_check, test_data_file_path, caplog):
        with caplog.at_level(logging.ERROR):
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
            mocked_file_check.side_effect = exceptions.RequestException
            # act
            extract(url, file_path_data, file_path_tracker, test_data_file_path)
            # assert
            assert "A RequestException occured:" in caplog.text

    @patch("src.extract.extract.os.path.isfile")
    def test_logs_failure_if_Exception_raised(self, mocked_file_check, test_data_file_path, caplog):
        with caplog.at_level(logging.ERROR):
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
            mocked_file_check.side_effect = Exception
            # act
            extract(url, file_path_data, file_path_tracker, test_data_file_path)
            # assert
            assert "An unexpected error occured:" in caplog.text
