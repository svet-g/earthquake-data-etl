import requests
import geojson
import json
import datetime
from src.utils.logging_utils import setup_logger

logger = setup_logger('extract_data_utils', 'extract_data_utils.log')

def extract_initial_month(url, file_path_data, file_path_tracker):
    '''
    params: 
        url (string) -> url string for the API call
        file_path (string) -> local path to save the file to
    returns: 
        {'time': current time in UTC format as expected by main USGS API endpoint}
    '''
    logger.info('Starting initial data extraction process of first month of earthquake data')
    # pull and save earthquake data from last 30 days to a local file at a specified file path in geojson format
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    with open(file_path_data, 'w') as f:
        geojson.dump(data, f)
    logger.info(
        f'Data extraction completed successfully! '
        f'Your data was saved to file {f.name} :)'
        )
    # create a last polled json file to track the time of last update and return the json from the function as well
    current_time_UTC = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S')
    last_poll_dict = {'time': current_time_UTC}
    with open(file_path_tracker, 'w') as f:
        json.dump(last_poll_dict, f)
    logger.info(f'Tracker file successful created - time: {current_time_UTC}, path: {f.name} :)')
    return last_poll_dict
