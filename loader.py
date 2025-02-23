import os

import requests
import json
import csv
from constants import *
class Loader:
    def __init__(self):
        self.coins_list_loc = 'data/readable_coin_data.json'

    @staticmethod
    def error_checker(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                for i in range(3):
                    func()
                print(f"Error fetching coin list after retries: {e}")
        return wrapper

    @error_checker
    def save_coins_list(self):
        url = f"{API_URL}/coins/list"
        response = requests.get(url)
        with open(self.coins_list_loc, 'w') as f:
            json.dump(response.json(), f, indent=4)


    @staticmethod
    def save_coin_data(coin_id):
        url = f"{API_URL}/coins/{coin_id}"
        response = requests.get(url)
        coin_info_file = f'data/{coin_id}_info.json'
        with open(coin_info_file, 'w') as f:
            json.dump(response.json(), f, indent=4)
        return coin_info_file

    def search_for_coin_id(self, name):
        with open(self.coins_list_loc, 'r') as f:
            all_coin_info = json.load(f)
        for coin in all_coin_info:
            if coin["name"] == name:
                return coin["id"]
        else:
            return None

    @staticmethod
    def set_up_price_history():
        if not os.path.exists("data/price_history.csv"):
            with open('data/price_history.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["day", "hour", "price hour ago"])


