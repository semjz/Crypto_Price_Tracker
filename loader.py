import json
from api_client import APIClient
from constants import DATA_DIR

class IDataLoader:
    """Interface for data loading."""
    def __init__(self):
        self.coins_list_loc = f"{DATA_DIR}readable_coin_data.json"

    def load_data(self):
        raise NotImplementedError

class CoinListLoader(IDataLoader):
    """Loads a list of available coins."""

    def load_data(self):
        data = APIClient.get("/coins/list")
        if data:
            with open(self.coins_list_loc, "w") as f:
                json.dump(data, f, indent=4)
        return data

class CoinDataLoader(IDataLoader):
    """Fetches data for a specific coin."""

    def __init__(self, coin_name):
        super().__init__()
        self.coin_id = self.search_for_coin_id(coin_name)

    def load_data(self):
        if not self.coin_id:
            print("Coin not found")
            return
        data = APIClient.get(f"/coins/{self.coin_id}")
        if data:
            file_path = f"{DATA_DIR}{self.coin_id}_info.json"
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            return file_path
        return None

    def search_for_coin_id(self, name):
        with open(self.coins_list_loc, 'r') as f:
            all_coin_info = json.load(f)
        for coin in all_coin_info:
            if coin["name"] == name.title():
                return coin["id"]
        else:
            return None