import os
import json
import csv
from datetime import datetime
class Tracker:
    def __init__(self):
        self.file_loc = 'data/readable_coin_data.json'
        self.file_to_visualise = 'data/tracked_data.json'
        self.set_up_price_history()

    # def price_history(self, file_name, currency):
    #     with open(file_name, 'r') as f:
    #         json_data = json.load(f)
    #         current_price = json_data["market_data"]["current_price"][currency]
    #         price_change_24h = json_data["market_data"]["price_change_24h_in_currency"][currency]
    #         price_change_percentage_7d = json_data["market_data"]["price_change_percentage_7d_in_currency"][currency]
    #         price_change_percentage_14d = json_data["market_data"]["price_change_percentage_14d_in_currency"][currency]
    #         price_24h = current_price - price_change_24h
    #         price_7d = self.calc_price(current_price, price_change_percentage_7d)
    #         price_14d = self.calc_price(current_price, price_change_percentage_14d)
    #
    #     with open(self.file_to_visualise, 'w') as f:
    #         json.dump({"current_price": current_price, "price_24h": price_24h, "price_7d":price_7d, "price_14d": price_14d}, f)

    def track_price_daily(self, file_name, currency):
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

    def refine_price(self, coin_id):
        with open(f'data/{coin_id}_info.json', 'r') as f:
            coin_data = json.load(f)
            current_price = coin_data["market_data"]["current_price"]

        with open(self.file_to_visualise, "w") as f:
            f.writelines([f"price in btc: {current_price['btc']}{os.linesep}",
                          f"price in usd: {current_price['usd']}{os.linesep}",
                          f"price in eur: {current_price['eur']}{os.linesep}"])

    @staticmethod
    def set_up_price_history():
        if not os.path.exists("data/price_history.csv"):
            with open('data/price_history.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["datetime", "price_hour_ago"])