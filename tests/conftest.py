import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
import json
import geopandas
import pandas as pd
from config.env_config import setup_env

def pytest_runtest_setup(item):
    """Ensure test environment is set before each test"""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    setup_env(["pytest", "test"])

@pytest.fixture
def prod_environment():
    setup_env(['run_etl', 'prod'])
    
    yield

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
def test_procesed_data_file_path():
    file_path = (
        Path(__file__).parent.parent
        / 'data'
        / 'test'
        / 'test_2025-08-19 16:19:08.416693_transformed_earthquake_data.json'
    )
    return file_path

@pytest.fixture
def test_processed_df(test_procesed_data_file_path):
    processed_df = pd.read_json(test_procesed_data_file_path)
    return processed_df

@pytest.fixture
def test_geojson(test_data_file_path):
    with test_data_file_path.open() as f:
        return json.load(f)

@pytest.fixture
def test_transform_gdf(test_data_file_path):
    gdf = geopandas.read_file(test_data_file_path)
    return gdf