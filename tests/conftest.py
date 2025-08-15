import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
import json

@pytest.fixture
def mocked_geojson():
    
    file_path = Path(__file__).parent.parent / 'data' / 'test' / 'unclean_earthquake_test_data.geojson'
    
    with file_path.open() as f:
        return json.load(f)