import requests
from constants import API_URL

class APIClient:
    """Handles API requests to CoinGecko"""

    @staticmethod
    def get(endpoint, params=None):
        url = f"{API_URL}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"API request failed: {e}")
            return None