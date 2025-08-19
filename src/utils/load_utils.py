import os
from sqlalchemy import create_engine

def db_engine(db='TARGET'):
    
    '''
    creates a database engine
    
    params: db (str) -> type of db: 'TARGET' or 'SOURCE' to complete the enviroment variable name string, defaults to 'TARGET'
    
    returns: a SQLAlchemy db engine
    
    '''
    
    user = os.getenv(f'{db}_DB_USER')
    password = os.getenv(f'{db}_DB_PASSWORD')
    host = os.getenv(f'{db}_DB_HOST')
    port = os.getenv(f'{db}_DB_PORT')
    database = os.getenv(f'{db}_DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    
    return engine