import os
from pathlib import Path
from requests.exceptions import JSONDecodeError, HTTPError, RequestException
from src.utils.logging_utils import setup_logger
from src.utils.extract_utils import extract_initial_month

logger = setup_logger("extract_data", "extract_data.log")

last_30_days_url = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
)
file_path_data_last_30_days = (
    Path(__file__).parent.parent.parent
    / "data"
    / "raw"
    / "earthquake-data-last-30-days.geojson"
)
file_path_tracker = (
    Path(__file__).parent.parent.parent / "src" / "extract" / "poll_tracker.json"
)


def extract(initial_poll_url, file_path_data, file_path_tracker):
    """
    params:
        url (string) -> url string for the API call
        file_path_data (string) -> local path to save the data file to
        file_path_tracker (string) -> local path to save the tracker file to
    returns:
        None
    """
    try:
        # if tracker file doesn't exists - use the extract intial month util
        # to get the initial data in as a geojson
        if not os.path.isfile(file_path_tracker):
            extract_initial_month(initial_poll_url, file_path_data, file_path_tracker)
        # if the file exists - do nothing -
        # other functionality will come if get to strech goals
        else:
            # strech goal: poll the API either on schedule or using an alert to trigger the extract function
            # this will use the tracker made in the extract_initial_month function to construct the string for the more general USGS API endpoint
            pass
    # handle exceptions relevent to the API call in extract_initial_month
    # as well as the generic expection last in case of anything unexpected
    # stretch goal: add retries under relevant exceptions or any other exception handling
    except JSONDecodeError as e:
        logger.exception(f"A JSONDecodeError occured: {e}", stack_info=True)
    except HTTPError as e:
        logger.exception(f"An HTTPError occured: {e}", stack_info=True)
    except RequestException as e:
        logger.exception(f"A RequestException occured: {e}", stack_info=True)
    except Exception as e:
        logger.exception(f"An unexpected error occured: {e}", stack_info=True)


if __name__ == "__main__":

    extract(last_30_days_url, file_path_data_last_30_days, file_path_tracker)
