import os

from dotenv import load_dotenv

from constants import *
import requests

class AuthHandler:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("COINGECKO_API_KEY")

    def authenticate(self):
        """Authenticates API key with CoinGecko"""
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": self.api_key,
        }
        response = requests.get(f"{API_URL}/ping", headers=headers)
        return response.status_code == 200