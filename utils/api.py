import requests

def get_search_filed(field_name: str, selections: dict = None):
    url = f"https://gw.yad2.co.il/search-options/vehicles/cars?fields={field_name}"

    if selections:
        for key, value in selections.items():
            url += f"&{key}={value}"

    response = requests.get(url)
    response_json = response.json()
    field = response_json['data'][field_name]
    return field

def search_recent_car_posts(user_selections: dict):
    url = "https://gw.yad2.co.il/feed-search-legacy/vehicles/cars?"

    base_query_params = {
        "page": 1,
        "forceLdLoad": True,
        "gearBox": 1,
        "Order": 5,
        "priceOnly": 1,
        "imgOnly": 1
    }

    for key, value in base_query_params.items():
        url += f"&{key}={value}"

    if user_selections:
        for key, value in user_selections.items():
            url += f"&{key}={value}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response = response.json()
    return response['data']['feed']['feed_items']