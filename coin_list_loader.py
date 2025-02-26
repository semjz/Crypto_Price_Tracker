import time

import requests
import json

from constants import *
class CoinListLoader:
    def __init__(self):
        self.coins_list_loc = 'data/readable_coin_data.json'

    @staticmethod
    def error_checker(func):
        def wrapper(*args, **kwargs):
            for _ in range(3):
                try:
                    func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    time.sleep(2)
                    print(f"Error fetching coin list after retries: {e}")
        return wrapper

    @error_checker
    def save_coins_list(self):
        url = f"{API_URL}/coins/list"
        response = requests.get(url)
        with open(self.coins_list_loc, 'w') as f:
            json.dump(response.json(), f, indent=4)