import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
import json
import geopandas


@pytest.fixture
def test_data_file_path():
    file_path = (
        Path(__file__).parent.parent
        / 'data'
        / 'test'
        / 'test_earthquake_data_last_30_days.geojson'
    )
    return file_path

@pytest.fixture
def test_geojson(test_data_file_path):
    with test_data_file_path.open() as f:
        return json.load(f)

@pytest.fixture
def test_extracted_dataframe(test_data_file_path):
    gdf = geopandas.load_file(test_data_file_path)
    return gdf