import os
import sys
from config.env_config import setup_env
from pathlib import Path
from datetime import datetime
from src.extract.extract import extract
from src.transform.transform import transform
from src.load.load import load
from src.utils.load_utils import db_engine


def main():
    # initialise required params
        
    last_30_days_url = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    )
    
    file_path_data_last_30_days = (
    Path(__file__).parent.parent
    / "data"
    / "raw"
    / "earthquake_data_last_30_days.geojson"
    )
    
    file_path_tracker = (
    Path(__file__).parent.parent / "src" / "extract" / "poll_tracker.json"
    )

    file_path_sample = (
        Path(__file__).parent.parent
        / "data"
        / "test"
        / "test_earthquake_data_last_30_days.geojson"
    )
    
    file_name_transformed_data = f'{datetime.now()}_transformed_earthquake_data.json'
    file_path_transformed_data = Path(__file__).parent.parent / 'data' / 'processed' / file_name_transformed_data
    
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
    engine = db_engine()
    table_name = 'earthquakes-svet-g'
    schema = 'de_2506_a'
    mode = 'replace'
    # Get the argument from the run_etl command and set up the environment
    setup_env(sys.argv)
    # execute extract, transform and load
    extract(last_30_days_url, file_path_data_last_30_days, file_path_tracker, file_path_sample)
    df = transform(file_path_data_last_30_days, file_path_transformed_data, columns_to_drop)
    load(df, engine, table_name, schema, mode)
    print(
        f"ETL pipeline run successfully in " f"{os.getenv('ENV', 'error')} environment!"
    )

if __name__ == "__main__": # pragma: no cover
    
    # last_30_days_url = (
    # "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    # )
    
    # file_path_data_last_30_days = (
    # Path(__file__).parent.parent.parent
    # / "data"
    # / "raw"
    # / "earthquake-data-last-30-days.geojson"
    # )
    
    # file_path_tracker = (
    # Path(__file__).parent.parent.parent / "src" / "extract" / "poll_tracker.json"
    # )

    # file_path_sample = (
    #     Path(__file__).parent.parent.parent
    #     / "data"
    #     / "test"
    #     / "test_earthquake_data_last_30_days.geojson"
    # )
    
    # file_path_raw_data = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'earthquake-data-last-30-days.geojson'
    
    # file_name_transformed_data = f'{datetime.now()}_transformed_earthquake_data.json'
    # file_path_transformed_data = Path(__file__).parent.parent.parent / 'data' / 'processed' / file_name_transformed_data
    
    # columns_to_drop = ['tz',
    #                     'detail',
    #                     'mmi',
    #                     'status',
    #                     'net',
    #                     'code',
    #                     'ids',
    #                     'sources',
    #                     'types',
    #                     'nst',
    #                     'dmin',
    #                     'rms',
    #                     'gap',
    #                     'type',
    #                     'title']
    
    main()
