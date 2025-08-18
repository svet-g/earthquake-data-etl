import geopandas
import json
from pathlib import Path
from datetime import datetime
from src.utils.logging_utils import setup_logger
from src.utils.transform_utils import drop_rows, drop_columns, standardise_formatting

logger = setup_logger("transform_data", "transform_data.log")

def transform(file_path_raw_data, file_path_transformed_data, columns_to_drop):
    try:
        gdf = geopandas.read_file(file_path_raw_data)
        gdf = drop_rows(gdf)
        gdf = drop_columns(gdf, columns_to_drop)
        df = standardise_formatting(gdf)
        df.to_json(file_path_transformed_data, indent=4)
        return df
    except Exception as e:
        logger.exception(f"An unexpected error occured: {e}", stack_info=True)

if __name__ == '__main__': # pragma: no cover
    
    file_path_raw_data = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'earthquake-data-last-30-days.geojson'
    
    file_name_transformed_data = f'{datetime.now()}_transformed_earthquake_data.json'
    file_path_transformed_data = Path(__file__).parent.parent.parent / 'data' / 'processed' / file_name_transformed_data
    
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
    
    transform(file_path_raw_data, file_path_transformed_data, columns_to_drop)