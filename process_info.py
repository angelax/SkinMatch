import scrap_sephora

scraper = scrap_sephora.SephoraScrap('moisturizer')
products = scraper.scrap()
approved_list = []
avoid_list = ['lavender', 'lavandula', 'rose', 'rosa', 'sulfate', 'honey', 'alcohol']

for k in products:
    invalid = False
    for i1 in products[k]['ingredients']:
        for i2 in avoid_list:
            if i2 in i1.lower():
                invalid = True
                break
        if invalid:
            break
    if not invalid:
        approved_list.append(products[k])
        print(products[k]['brand'] + " " + products[k]['name'] + " " + 'https://www.sephora.com' + k)

