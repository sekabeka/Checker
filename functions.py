import requests

from typing import List, Dict

api_token = "e495563786-43397eca9e-2553afcc35"

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
