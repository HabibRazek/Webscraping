from urllib.parse import urljoin
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

def search(request):
    # Retrieve the list of phone brands
    brands = []
    smartphones = []

    for i in range(0, 1):
        url = f"https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page={i}#catalog-listing"
        response = requests.get(url)
        response = response.content
        soup = BeautifulSoup(response, 'html.parser')

        # Extract articles bloc from the html
        div = soup.find('div', class_='-paxs row _no-g _4cl-3cm-shs')
        articles = div.find_all('article', class_='prd _fb col c-prd')

        if request.method == 'POST':
            # Retrieve the selected brand and price from the form
            brand = request.POST.get('brand')
            price = request.POST.get('price')
        
        for article in articles:
            title = article.find('div', class_='info')
            phone_name = title.find('h3', class_='name').text
            marque = phone_name.strip()
            phone_brand = marque.split()[0]
            prix = title.find('div', class_='prc').text
            phone_price = prix.replace(',', '').replace('.', '').replace('TND', '')
            phone_price = float(phone_price) / 100
            image = article.find('div', class_='img-c')
            phone_img = image.find('img', class_='img')['data-src']
            phone_link = article.find('a', {'class':'core'}).get('href')
            link = urljoin('https://www.jumia.com.tn/', phone_link)


            if phone_brand not in brands:
               brands.append(phone_brand)

            if request.method == 'POST':
                if brand == '' or phone_brand.lower() == brand.lower():
                   if price == '' or float(phone_price) <= float(price):
                       smartphones.append({'brand': phone_brand, 'name': phone_name, 'price': phone_price, 'img': phone_img, 'phone_link': link})
            else :
               smartphones.append({'brand': phone_brand, 'name': phone_name, 'price': phone_price, 'img': phone_img, 'phone_link': link})



    # Render with the appropriate values
    if request.method == 'POST':
      return render(request, 'search.html', {'brands': brands, 'phones': smartphones, 'selected_brand': brand, 'selected_price': price})
    return render(request, 'search.html', {'brands': brands, 'phones': smartphones})

