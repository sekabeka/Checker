import requests
import os

from typing import List, Dict

api_token = os.getenv('API_TOKEN')

def get_proxy() -> List[Dict[str, str]]:
    result = []
    response = requests.get(
        url=f"https://proxy6.net/api/{api_token}/getproxy"
    )
    for d in response.json()['list'].values():
        result.append({
            'username' : d["user"],
            'password' : d["pass"],
            'port' : d["port"],
            'host' : d["host"]
        })
    return result
