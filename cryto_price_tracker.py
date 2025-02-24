import threading

from dotenv import load_dotenv
import os
import requests
from loader import Loader
from tracker import Tracker
from visualizer import Visualizer
from constants import *



def authenticate(api_key):
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key
    }
    url = f"{api_url}/ping"
    response = requests.get(url, headers=headers)
    return response

load_dotenv()
API_KEY = os.getenv("COINGECKO_API_KEY")
api_url = "https://api.coingecko.com/api/v3"

def main():
    # Check API Authentication
    resp = authenticate(API_KEY)
    if resp.status_code == 200:
        print("Pong!")
        l = Loader()
        l.save_coins_list()
        name = input("Enter Coin Name: ")
        coin_id = l.search_for_coin_id(name.title())
        if coin_id:
            update_chart(l, coin_id)
        else:
            print("Coin not found")
    else:
        print(resp.json())

def update_chart(loader, coin_id):
    file_name = loader.save_coin_data(coin_id)
    tracker = Tracker()
    tracker.track_price_daily(file_name, "usd")
    if coin_id:
        loader.save_coin_data(coin_id)
        v = Visualizer()
        v.visualize()
    threading.Timer(TIME_INTERVAL, update_chart, args=(loader, coin_id)).start()

if __name__ == '__main__':
    main()

