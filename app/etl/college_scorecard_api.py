import requests
import time
import random
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_college_data(api_key, fields, page_limit=None):
    """
    Retrieves data from the College Scorecard API.

    This function fetches data for a set of specified fields from the College Scorecard API.
    It paginates through results and collects data up to a specified page limit.

    Parameters:
        api_key (str): The API key for accessing the College Scorecard API.
        fields (list): A list of strings representing the fields to be retrieved.
        page_limit (int, optional): The maximum number of pages to fetch. If None, fetches all available data.

    Returns:
        dict: A dictionary where each key is a field, and the value is a list of data for that field.
    """

    logging.info("Starting to fetch data from College Scorecard API.")
    base_url = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
    data_dictionary = {field: [] for field in fields}  # Dictionary to store the data
    page_num = 0

    while True:
        api_request = f"{base_url}?fields={','.join(fields)}&api_key={api_key}&page={page_num}&per_page=100"
        try:
            response = requests.get(api_request)
            response.raise_for_status()
            data = response.json()

            if not data["results"] or (page_limit and page_num >= page_limit):
                logging.info("No more results found or page limit reached.")
                break

            for school in data["results"]:
                for field in fields:
                    data_dictionary[field].append(school.get(field, None))

            logging.info(f"Fetched page {page_num} successfully.")
            page_num += 1
            time.sleep(random.randint(0, 3))
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP Error occurred: {err}")
            break
        except requests.exceptions.RequestException as err:
            logging.error(f"Request failed: {err}")
            break
        except ValueError as err:
            logging.error(f"Error parsing JSON response: {err}")
            break

    logging.info("Data fetching process completed.")
    return data_dictionary
