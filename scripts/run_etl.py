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
    # set up the env
    setup_env(sys.argv)
    env = os.getenv('ENV', '')
    
    # declare variables for all envs
    engine = db_engine()
    table_name = 'earthquakes-svet-g'
    mode = 'replace'
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
    
    # declare those vars that are env specific and run the extract, trasnform and load in each
    if env in ['test', 'dev']:
        schema = None
        url = 'fake url'
        test_raw_path = (Path(__file__).parent.parent / 'data' / 'test' / 'test_earthquake_data_last_30_days.geojson')
        test_tracker_path = (Path(__file__).parent.parent / 'data' / 'test' / 'test_tracker.json')
        test_sample_path = (Path(__file__).parent.parent / 'data' / 'test' / 'test_sample.geojson')
        test_transformed_path = (Path(__file__).parent.parent / 'data' / 'test' / 'test_transformed.json')
        extract(url, test_raw_path, test_tracker_path, test_sample_path)
        df = transform(test_raw_path, test_transformed_path, columns_to_drop)
        load(df, engine, table_name, schema, mode)
        print(
            f"ETL pipeline run successfully in " f"{os.getenv('ENV', 'error')} environment!"
        )
    
    elif env == 'prod':
        schema = 'de_2506_a'
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
        extract(last_30_days_url, file_path_data_last_30_days, file_path_tracker, file_path_sample)
        df = transform(file_path_data_last_30_days, file_path_transformed_data, columns_to_drop)
        load(df, engine, table_name, schema, mode)
        print(
            f"ETL pipeline run successfully in " f"{os.getenv('ENV', 'error')} environment!"
        )
if __name__ == "__main__": # pragma: no cover
    main()
