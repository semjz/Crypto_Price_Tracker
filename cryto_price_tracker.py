from dotenv import load_dotenv
import os
import requests
import json


def save_coin_list():
    try:
        url = f"{api_url}/coins/list"
        response = requests.get(url)
        with open(all_coin_info_file, 'w') as f:
            json.dump(response.json(), f, indent=4)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coin list: {e}")

def search_for_coin_id(name):
    with open(all_coin_info_file, 'r') as f:
       all_coin_info = json.load(f)
    for coin in all_coin_info:
        if coin["name"] == name:
            return coin["id"]
    else:
        return None

def save_coin_data(coin_id):
    url = f"{api_url}/coins/{coin_id}"
    response = requests.get(url)
    coin_info_file = f'data/{coin_id}_info.json'
    with open(coin_info_file, 'w') as f:
        json.dump(response.json(), f, indent=4)

def refine_price(coin_id):
    with open(f'data/{coin_id}_info.json', 'r') as f:
        coin_data = json.load(f)
        current_price = coin_data["market_data"]["current_price"]
    print(f"price in btc: {current_price['btc']}")
    print(f"price in usd: {current_price['usd']}")
    print(f"price in eur: {current_price['eur']}")

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
all_coin_info_file = 'data/readable_coin_data.json'

def main():
    # Check API Authentication
    resp = authenticate(API_KEY)
    if resp.status_code == 200:
        print("Pong!")
        save_coin_list()
        name = input("Enter Coin Name: ")
        coin_id = search_for_coin_id(name)
        if coin_id:
            save_coin_data(coin_id)
            refine_price(coin_id)
        else:
            print("Coin not found")
    else:
        print(resp.json())

if __name__ == '__main__':
    main()

