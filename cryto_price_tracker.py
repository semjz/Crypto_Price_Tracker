import threading

from loader import CoinListLoader, CoinDataLoader
from tracker import PriceTracker
from visualizer import Visualizer
from constants import *
from auth import AuthHandler
from util import set_up_price_history


def update_chart(file_name):
    tracker = PriceTracker()
    tracker.track_price(file_name, "usd")
    v = Visualizer()
    v.visualize()
    threading.Timer(TIME_INTERVAL, update_chart, args=(file_name,)).start()



def main():
    # Check API Authentication
    auth = AuthHandler()
    if not auth.api_key:
        raise ValueError("API Key is missing. Set it in the .env file.")

    if not auth.authenticate():
        print("authentication failed, api_key not correct")
        return

    print("Pong!")
    set_up_price_history()
    cll = CoinListLoader()
    cll.load_data()

    name = input("Enter Coin Name: ")
    cdl = CoinDataLoader(name.title())
    file_name = cdl.load_data()
    if file_name:
        update_chart(file_name)
    else:
        print("Coin not found.")

if __name__ == '__main__':
    main()

