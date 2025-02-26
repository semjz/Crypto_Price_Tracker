import os
import json
import csv
from datetime import datetime

from constants import DATA_DIR


class ITracker:
    """Interface for price tracking."""

    def track_price(self, file_name, currency):
        raise NotImplementedError

class PriceTracker(ITracker):
    """Tracks price history and saves to CSV."""

    def track_price(self, file_name, currency):
        with open(file_name, 'r') as f:
            json_data = json.load(f)
            current_price = json_data["market_data"]["current_price"][currency]
            price_change_percentage_1h = json_data["market_data"]["price_change_percentage_1h_in_currency"][currency]
            price_1h = self.calc_price(current_price, price_change_percentage_1h)
            with open('data/price_history.csv', 'a', newline='') as f:
                now = datetime.now()
                current_date = now.date()
                current_time = f"{now.strftime("%H")}:{now.strftime("%M")}"
                writer = csv.writer(f)
                writer.writerow([f"{current_date} {current_time}", price_1h])

    @staticmethod
    def calc_price(current_price, percent_diff):
        return current_price * (1 + (-1 * (percent_diff / 100)))

class PriceRefiner:
    """Refines and formats price data."""

    @staticmethod
    def refine_price(coin_id):
        with open(f"{DATA_DIR}{coin_id}_info.json", "r") as f:
            coin_data = json.load(f)
            current_price = coin_data["market_data"]["current_price"]

        return {
            "btc": current_price["btc"],
            "usd": current_price["usd"],
            "eur": current_price["eur"]
        }


