import os
from sqlalchemy import Engine
from src.utils.load_utils import db_engine

class TestDBEngine:
    def test_returns_sqlalchemy_engine_type(self):
        # debug
        import os
        print(f"ENV: {os.getenv('ENV')}")
        print(f"TARGET_DB_NAME: {os.getenv('TARGET_DB_NAME')}")
        print(f"TARGET_DB_PORT: {os.getenv('TARGET_DB_PORT')}")
        print(f"TARGET_DB_HOST: {os.getenv('TARGET_DB_HOST')}")
        # act
        return_value = db_engine()
        # assert 
        assert isinstance(return_value, Engine)