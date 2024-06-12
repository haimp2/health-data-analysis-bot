import requests

def search_recent_car_posts():
    url = "https://gw.yad2.co.il/feed-search-legacy/vehicles/cars"
    query_params = {
        "manufacturer": "Toyota",
        "model": "Corolla",
        "year": "2015",
        "price": "10000-15000",
        "priceType": "1",
        "owner": "1",
        "img": "1",
        "limit": "10",
        "page": "1",
        "sort": "1"
    }
    response = requests.get(url, params=query_params)
    return response.json()