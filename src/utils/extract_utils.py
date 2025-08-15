import requests
import geojson
from src.utils.logging_utils import setup_logger

logger = setup_logger('extract_data', 'extract_data.log')

def extract_initial_month(url, file_path):
    '''
    params: 
        url (string) -> url string for the API call
        file_path (string) -> local path to save the file to
    returns: 
        None
    '''
    try:
        logger.info('Starting initial data extraction process of first month of earthquake data')
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        with open(file_path, 'w') as f:
            geojson.dump(data, f)
        logger.info(
            f'Data extraction completed successfully!'
            f'Your data was saved to file {f} :)'
            )
        # see if makes sense to return something out of here
    # could make a custom exception class to then raise out of this function under each except to then tigger retries
    except requests.exceptions.HTTPError as e:
        logger.exception(f'An HTTPError occured: {e}', stack_info=True)
    except requests.exceptions.RequestException as e:
        logger.exception(f'A RequestException occured: {e}', stack_info=True)