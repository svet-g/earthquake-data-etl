from sqlalchemy import Engine
from src.utils.load_utils import db_engine

class TestDBEngine:
    def test_returns_sqlalchemy_engine_type(self):
        # act
        return_value = db_engine()
        # assert 
        assert isinstance(return_value, Engine)