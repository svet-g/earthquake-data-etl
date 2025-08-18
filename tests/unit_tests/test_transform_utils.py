import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
import json
import logging
from requests import exceptions
import datetime
import numpy as np
import pandas as pd
from src.utils.transform_utils import drop_rows, drop_columns, standardise_formatting

class TestDropsRowsandColumns:
    def test_drops_specified_rows(self, test_transform_gdf):
        # arrange
        expected_non_earthquake_type_count = 0
        expected_gap_above_180_count = 0
        expected_gap_is_null_count = 0
        expected_duplicates = 0
        
        # act
        actual = drop_rows(test_transform_gdf)
        actual_type = actual[actual['type'] != 'earthquake']
        actual_non_earthquake_type_count = actual_type['id'].count()
        
        actual_gap_above_180 = actual[actual['gap'] > 180]
        actual_gap_above_180_count = actual_gap_above_180['id'].count()
        
        actual_gap_is_null = actual[actual['gap'].isna()]
        actual_gap_is_null_count = actual_gap_is_null['id'].count()
        
        actual_duplicates = len(actual['id'])-len(actual['id'].drop_duplicates())
        
        # assert
        assert expected_non_earthquake_type_count == actual_non_earthquake_type_count
        assert expected_gap_above_180_count == actual_gap_above_180_count
        assert expected_gap_is_null_count == actual_gap_is_null_count
        assert expected_duplicates == actual_duplicates
        
    def test_drops_specified_columns(self, test_transform_gdf):
        # arrange
        expected_columns = ['id',
                            'mag',
                            'place',
                            'time',
                            'updated',
                            'url',
                            'felt',
                            'cdi',
                            'alert',
                            'tsunami',
                            'sig',
                            'magType',
                            'geometry']
        
        columns_to_drop = ['tz',
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
        # act
        result = drop_columns(test_transform_gdf, columns_to_drop)
        actual_columns = [column for column in result.columns]
        # assert
        assert expected_columns == actual_columns
        
class TestStandardiseFormatting:
    def test_changes_unix_epoch_to_datetime(self, test_transform_gdf):
        # act
        gdf = standardise_formatting(test_transform_gdf)
        # assert
        assert isinstance(gdf['time'][0], datetime.datetime)
        assert isinstance(gdf['updated'][0], datetime.datetime)
    
    def test_creates_boolean_columns_where_required(self, test_transform_gdf):
        # act
        gdf = standardise_formatting(test_transform_gdf)
        # assert
        assert isinstance(gdf['tsunami'][0], np.bool)
    
    def test_changes_geometry_to_longitude_latitude_and_depth(self, test_transform_gdf):
        # arrange
        expected_included_columns = ['longitude', 'latitude', 'depth']
        # act
        df = standardise_formatting(test_transform_gdf)
        # assert
        assert all([column in df.columns for column in expected_included_columns])
    
    def test_returns_a_pandas_df(self, test_transform_gdf):
        # act
        df = standardise_formatting(test_transform_gdf)
        # assert
        assert isinstance(df, pd.DataFrame)