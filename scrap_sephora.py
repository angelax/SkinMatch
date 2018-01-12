import requests
import json
import re
from bs4 import BeautifulSoup

option_url = {'moisturizer':'moisturizing-cream-oils-mists',
       'cleanser':'cleanser',
       'treatment':'facial-treatments',
       'mask':'face-mask',
       'eye cream':'eye-treatment-dark-circle-treatment',
       'sunscreen':'sunscreen-sun-protection',
       'lip care':'lip-treatments'
       }
base_url = 'https://www.sephora.com/'

# set option to search for different products on sephora
class SephoraScrap:
    def __init__(self, option):
        self.option = option

    def scrap(self):
        page = requests.get(base_url + option_url[self.option] + '?pageSize=-1')

        # Create a BeautifulSoup object
        soup = BeautifulSoup(page.text, 'html.parser')
        data = soup.find("script", {"id": "searchResult"})
        products = json.loads(data.next)

        product_list = {}

        for p in products['products']:
            key = p['product_url']
            detail_page = requests.get(base_url + key)

            ingredientsResult = re.search(r'\"ingredientDesc\":\"(.*?)\"', detail_page.text)
            data = []
            if ingredientsResult is not None:
                ingredientsDes = ingredientsResult.group(1)
                data = ingredientsDes.replace('.','').replace(' ','').split('<br>')
            ingredients = []
            for line in data:
                if line != "":
                    i = line.split(",")
                    if len(i) > 5:
                        ingredients = i

            product_list[key] = {
                'rating': p['rating'],
                'brand': p['brand_name'],
                'id': p['id'],
                'name': p['display_name'],
                'ingredients': ingredients
            }

        return product_list

