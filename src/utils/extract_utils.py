import requests
import geojson
import json
import datetime
from pathlib import Path
from src.utils.logging_utils import setup_logger

logger = setup_logger("extract_data_utils", "extract_data_utils.log")


def extract_initial_month(url, file_path_data, file_path_tracker):
    """
    params:
        url (string) -> url string for the API call
        file_path (string) -> local path to save the file to
    returns:
        {'time': current time in UTC format as expected by main USGS API endpoint}
    """
    logger.info(
        "Starting initial data extraction process of first month of earthquake data"
    )
    # pull and save earthquake data from last 30 days to a local file at a specified file path in geojson format
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    with open(file_path_data, "w") as f:
        geojson.dump(data, f)
    logger.info(
        f"Data extraction completed successfully! "
        f"Your data was saved to file {f.name} :)"
    )
    # create a last polled json file to track the time of last update and return the json from the function as well
    current_time_UTC = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S")
    last_poll_dict = {"time": current_time_UTC}
    with open(file_path_tracker, "w") as f:
        json.dump(last_poll_dict, f)
    logger.info(
        f"Tracker file successful created - time: {current_time_UTC}, path: {f.name} :)"
    )
    return last_poll_dict

# def duplicate_original_data(file_path_read, file_path_write):
#     '''
#     creates a testing copy with indented view of the loaded geojson
#     '''
#     with open(file_path_read, 'r') as f:
#         loaded_file = json.load(f)
#     with open(file_path_write, 'w') as f:
#         json.dump(loaded_file, f, indent=4)

def extract_sample(file_path_read, file_path_write):
    '''
    
    creates a small ten row sample of the original json and saves it to a local file and returns the json
    
    params:
        file_path_read (string) -> a file path to json file to retrive a sample from
        file_path_write (string) -> a file path to save the sample of the data that will be used for testing
        
    returns:
        a JSON of a sample of the original dataframe - total 10 rows with forced duplication
        to use for testing

    '''
    
    # load original ingested data
    with open(file_path_read, 'r') as f:
        data = json.load(f)
    
    # take a sample of first 5 earthquakes and duplicate them
    data['features'] = data['features'][:5] * 2
    
    # dump data into a test file
    with open(file_path_write, 'w') as f:
        json.dump(data, f, indent=4)
        
    return data
