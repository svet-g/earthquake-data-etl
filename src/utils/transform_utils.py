import geopandas

def drop_rows(gdf):
    '''
    clean up rows where type != 'earthquake and 'gap' is null or greater than 180 to improve accuracy of the location and depth data
    '''
    gdf = gdf[gdf['type'] == 'earthquake']
    gdf = gdf.dropna(subset=['gap'])
    gdf = gdf[gdf['gap'] < 180]
    return gdf

def drop_columns(gdf, columns_to_drop):
    '''
    params:
        gdf (gpd.DataFrame) - geopandas dataframe to be transformed
        columns_to_drop (list) - a python list of columns that need to be removed
    '''
    gdf.drop(columns_to_drop, axis=1, inplace=True)
    return gdf

# can add fillna()s for alerts, cdi and felt (these seems to be for very minor earthquakes so makes sense they are null - but double check!)