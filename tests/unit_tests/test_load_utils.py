from sqlalchemy import Engine
from config.env_config import setup_env
from src.utils.load_utils import db_engine

class TestDBEngine:
    def test_returns_sqlalchemy_engine_type_in_test_and_dev_envs(self):
        # test env
        # act
        return_value = db_engine()
        # assert 
        assert isinstance(return_value, Engine)
        
    def test_returns_sqlalchemy_engine_type_in_prod_env(self, prod_environment):
        # prod env
        return_value = db_engine()
        assert isinstance(return_value, Engine)
        