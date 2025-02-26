import requests
import json
from constants import *
class CoinDataLoader:
    def __init__(self):
        self.coins_list_loc = 'data/readable_coin_data.json'

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




