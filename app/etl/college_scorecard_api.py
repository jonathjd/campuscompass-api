import requests
import time
import random
from dotenv import load_dotenv
import os

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

    base_url = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
    data_dictionary = {field: [] for field in fields}  # Dictionary to store the data
    page_num = 0

    while True:
        api_request = f"{base_url}?fields={','.join(fields)}&api_key={api_key}&page={page_num}&per_page=100"
        response = requests.get(api_request)
        data = response.json()

        # Break the loop if no results or reached the page limit
        if not data["results"] or (page_limit and page_num >= page_limit):
            break

        # Process each school in the response
        for school in data["results"]:
            for field in fields:
                data_dictionary[field].append(school.get(field, None))

        page_num += 1
        time.sleep(random.randint(0, 3))

    return data_dictionary
