import csv
import os


def set_up_price_history():
    if not os.path.exists("data/price_history.csv"):
        with open('data/price_history.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["datetime", "price_hour_ago"])