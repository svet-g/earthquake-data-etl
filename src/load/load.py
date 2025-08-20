'''
id - varchar
mag - float
place - text
time - timestamp
updated - timestamp
url - text
felt - float
cdi - float
alert - varchar
tsunami - bool
sig - bigint
magtype - varchar
geometry - break up and put back together for streamlit
'''

def load(df, engine, table_name, schema, mode):
    '''
    
    loads pandas dataframe to a specified table and schema, creates table if doesn't exists, ovewrite entirely if it does exist
    
    params:
        df (pd.DataFrame) - dataframe to load
        table_name (str) - the name of the table to load to
        schema (str) - schema name to load to
        mode (str) - 'fail', 'replace' or 'append' - same as arguments for 'if_exits' in pandas DataFrame.to_sql
    
    '''

    with engine.connect() as connection:
        if schema is None:
            df.to_sql(table_name, connection, if_exists=mode, index=False)
        else:
            df.to_sql(table_name, connection, schema=schema, if_exists=mode, index=False)
        
        # FROM DOCS - just how to use the result
        # result = connection.execute(text("select username from users"))
        # for row in result:
        #     print("username:", row.username)