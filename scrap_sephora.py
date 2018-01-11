import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import * 
import requests
import json
import re
import pickle
from bs4 import BeautifulSoup
import urllib

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


#url = "https://www.sephora.com/facial-treatment-essence-P375849"
#detail_page = requests.get(url)
#ingredients = re.search(r'\"ingredientDesc\":\"(.*?)\"',detail_page.text).group(1)
#json_text = find_between(detail_page.text, '\"ingredientDesc\":\"', '\"' )


url = 'https://www.sephora.com/moisturizing-cream-oils-mists?pageSize=-1'
base_url = 'https://www.sephora.com'
min_ingredients = 5
page = requests.get(url)
# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')
data = soup.find("script", {"id": "searchResult"})
products = json.loads(data.next)
avoid_list = ['alcohol','rose','lavender','cone','fragrance','parfum','mineral oil']

product_list = {}
print(len(products['products']))

for p in products['products']:
    key = p['product_url']
    detail_page = requests.get(base_url + key)
    ingredientsDes = re.search(r'\"ingredientDesc\":\"(.*?)\"', detail_page.text).group(1)
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
    break

approved_list = []

for k in product_list:
    invalid = False
    for i1 in product_list[k]['ingredients']:
        for i2 in avoid_list:
            if i2 in i1.lower():
                invalid = True
                break
        if invalid:
            break
    if not invalid:
        approved_list.append(product_list[k])

print(approved_list)



