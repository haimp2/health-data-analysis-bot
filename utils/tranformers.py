def create_car_post(single_post: dict):

    base_ad_url = 'https://www.yad2.co.il/s/c/'

    return f'''
    New Car Post!

    Model: {single_post['manufacturer']} {single_post['model']}
    Year: {single_post['year']}
    Price: {single_post['price']}
    Kilometers: {single_post['kilometers']}
    Hand: {single_post['Hand_text']}
    Link: {base_ad_url}/{single_post['id']}
    '''


def filter_search_response(response: list):
    return list(filter(lambda x: x.get('ad_type') == 'ad' and not x.get('is_business'), response))