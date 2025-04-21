import requests

def get_breweries_metadata():
    url = "https://api.openbrewerydb.org/v1/breweries/meta"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Request failed with status code {response.status_code}"
            f" and message: {response.text}"
        )
