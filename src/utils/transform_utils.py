import geopandas
import pandas as pd

def drop_rows(gdf):
    '''
    clean up rows where type != 'earthquake and 'gap' is null or greater than 180 to improve accuracy of the location and depth data
    order dataframe by coordinates and drop any duplicates
    '''
    gdf = gdf[gdf['type'] == 'earthquake']
    gdf = gdf.dropna(subset=['gap'])
    gdf = gdf[gdf['gap'] < 180]
    gdf["geometry"] = gdf.normalize()
    gdf.drop_duplicates(inplace=True)
    return gdf

def drop_columns(gdf, columns_to_drop):
    '''
    params:
        gdf (gpd.DataFrame) - geopandas dataframe to be transformed
        columns_to_drop (list) - a python list of columns that need to be removed
    '''
    gdf.drop(columns_to_drop, axis=1, inplace=True)
    return gdf


def standardise_formatting(gdf):
    # break up geometry
    gdf['longitude'] = gdf['geometry'].x
    gdf['latitude'] = gdf['geometry'].y
    gdf['depth'] = gdf['geometry'].z
    df = gdf.drop(['geometry'], axis=1)
    # change tsunami to boolean values
    df['tsunami'] = df['tsunami'].astype('bool')
    # change unix time to timestamps
    df['time'] = pd.to_datetime(df['time'], utc=True, unit='ms')
    df['updated'] = pd.to_datetime(df['updated'], utc=True, unit='ms')
    return df

def asign_depth_bucket(depth):
    if depth < 60:
        return 'shallow'
    elif 300 > depth > 60:
        return 'intermediate'
    elif 700 > depth > 300:
        return 'deep'
    elif depth > 700:
        return 'highest_depth'

def aggregate_data(df, depth_buckets_func):
    # create a columns that calculates the difference between time of update and actual start time of the earthquake
    df['time_to_report'] = df['updated'] - df['time']
    # create a column that buckets depths into depth groups: shallow < 60 km, intermediate 60-300km, deep 300km-700km, highest_depth > 700 
    df['depth_group'] = df['depth'].apply(depth_buckets_func)
    return df

# can add fillna()s for alerts, cdi and felt (these seems to be for very minor earthquakes so makes sense they are null - but double check!)