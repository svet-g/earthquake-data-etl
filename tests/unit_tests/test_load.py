import os
from sqlalchemy import Engine
import pandas as pd
from sqlalchemy import text, create_engine
from src.utils.load_utils import db_engine
from src.load.load import load

class TestLoad:
    # currently pulling out json so the dates are in unix epoch cause to_json() removed it
    # need to check datetime format later
    def test_creates_specified_table_in_specified_schema_in_specified_db(self, test_processed_df):
        # arrange
        engine = create_engine("sqlite:///:memory:")
        table_name = 'test'
        schema = None
        mode = 'replace'
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
                            'longitude',
                            'latitude',
                            'depth',
                            'depth_group']
        # act
        load(test_processed_df, engine, table_name, schema, mode)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM test"))
            actual_columns = [col for col in result.keys()]
            # print(result.fetchone())
        # assert
        assert expected_columns == actual_columns
        