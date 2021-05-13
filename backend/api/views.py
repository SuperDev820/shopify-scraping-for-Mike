from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
# from api.models import Item
# from api.serializers import ItemSerializer
from rest_framework.decorators import api_view

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import time
from bs4 import BeautifulSoup

from pymongo import MongoClient

@api_view(['GET', 'POST', 'DELETE'])
def scrapOnLinux(request):
    if request.method == 'GET':
        print(request.GET.get('url'))
        base_url = request.GET.get('url')
        
    client = MongoClient('mongodb://localhost:27017/')
    db=client.admin
    
    page_url = base_url + "/collections/frontpage"

    options = Options()
    options.add_argument("--headless")
    options.add_argument('--window-size=1920, 1200')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options, executable_path='/home/mike/chromedriver')

    driver.get(page_url)
    time.sleep(5)
    driver.find_element_by_xpath("//button[@class='btn btn--tertiary btn--circle modal__close js-modal-close text-link']").click()
    time.sleep(1)
    first_page = BeautifulSoup(driver.page_source, 'html.parser')
    product_links = first_page.find_all('a', attrs={'class':'grid-product__link'})
    for i in range(0, 2):
        driver.get(base_url + product_links[i].attrs['href'])
        time.sleep(5)
        driver.find_element_by_xpath("//button[@class='btn btn--tertiary btn--full add-to-cart']").click()
        time.sleep(3)
    driver.find_element_by_xpath("//button[@class='btn btn--full cart__checkout cart__checkout--drawer']").click()
    time.sleep(5)

    email = 'random@gmail.com'
    first_name = 'asdf'
    last_name = 'fdsa'
    driver.find_element_by_id("checkout_email_or_phone").send_keys(email)
    time.sleep(1)
    driver.find_element_by_id("checkout_shipping_address_first_name").send_keys(first_name)
    time.sleep(1)
    driver.find_element_by_id("checkout_shipping_address_last_name").send_keys(last_name)
    time.sleep(1)
    countries = ['United States', 'Canada']
    states = ['California', 'Quebec']
    cities = ['Los Angeles', 'quebec']
    zip_codes = ['90036', 'G2E 5W3']
    addresses = ['350 South Fuller Avenue', '6515 boul Wilfrid-Hamel']
    for i in range(0, len(countries)):
        driver.find_element_by_id("checkout_shipping_address_country").send_keys(countries[i])
        time.sleep(1)
        driver.find_element_by_id("checkout_shipping_address_province").send_keys(states[i])
        time.sleep(1)
        driver.find_element_by_id("checkout_shipping_address_zip").clear()
        driver.find_element_by_id("checkout_shipping_address_zip").send_keys(zip_codes[i])
        time.sleep(1)
        driver.find_element_by_id("checkout_shipping_address_city").clear()
        driver.find_element_by_id("checkout_shipping_address_city").send_keys(cities[i])
        time.sleep(1)
        driver.find_element_by_id("checkout_shipping_address_address1").clear()
        driver.find_element_by_id("checkout_shipping_address_address1").send_keys(addresses[i])
        time.sleep(1)
        driver.find_element_by_id("continue_button").click()
        time.sleep(3)
        shipping_page = BeautifulSoup(driver.page_source, 'html.parser')
        cheapest_shipping_price = shipping_page.find_all('span', attrs={'class':'radio__label__accessory'})[0].text.strip()
        print(cheapest_shipping_price)
        #Insert data object directly into MongoDB via isnert_one
        data = {
            'country' : countries[i],
            'price' : cheapest_shipping_price
        }
        result=db.reviews.insert_one(data)

        prev_link = shipping_page.find('a', attrs={'class':'step__footer__previous-link'})
        driver.get(base_url + prev_link.attrs['href'])
        time.sleep(3)
    driver.quit()
    return JsonResponse({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST', 'DELETE'])
def scrapOnWindow(request):
    client = MongoClient('mongodb://localhost:27017/')
    db=client.admin

    base_url = "https://afiafoods.com"
    page_url = "https://afiafoods.com/collections/frontpage"

    options = Options()
    options.headless = False
    options.add_argument('--window-size=1920, 1200')
    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")

    driver.get(page_url)
    time.sleep(5)
    driver.find_element_by_xpath("//button[@class='btn btn--tertiary btn--circle modal__close js-modal-close text-link']").click()
    time.sleep(1)
    first_page = BeautifulSoup(driver.page_source, 'html.parser')
    product_links = first_page.find_all('a', attrs={'class':'grid-product__link'})
    for i in range(0, 2):
        driver.get(base_url + product_links[i].attrs['href'])
        time.sleep(5)
        driver.find_element_by_xpath("//button[@class='btn btn--tertiary btn--full add-to-cart']").click()
        time.sleep(3)
    driver.find_element_by_xpath("//button[@class='btn btn--full cart__checkout cart__checkout--drawer']").click()
    time.sleep(5)

    email = 'random@gmail.com'
    first_name = 'asdf'
    last_name = 'fdsa'
    driver.find_element_by_id("checkout_email_or_phone").send_keys(email)
    time.sleep(1)
    driver.find_element_by_id("checkout_shipping_address_first_name").send_keys(first_name)
    time.sleep(1)
    driver.find_element_by_id("checkout_shipping_address_last_name").send_keys(last_name)
    time.sleep(1)
    countries = ['United States', 'Canada']
    states = ['California', 'Quebec']
    cities = ['Los Angeles', 'quebec']
    zip_codes = ['90036', 'G2E 5W3']
    addresses = ['350 South Fuller Avenue', '6515 boul Wilfrid-Hamel']
    for i in range(0, len(countries)):
        driver.find_element_by_id("checkout_shipping_address_country").send_keys(countries[i])
        time.sleep(1)
        driver.find_element_by_id("checkout_shipping_address_province").send_keys(states[i])
        time.sleep(1)
        driver.find_element_by_id("checkout_shipping_address_zip").clear()
        driver.find_element_by_id("checkout_shipping_address_zip").send_keys(zip_codes[i])
        time.sleep(1)
        driver.find_element_by_id("checkout_shipping_address_city").clear()
        driver.find_element_by_id("checkout_shipping_address_city").send_keys(cities[i])
        time.sleep(1)
        driver.find_element_by_id("checkout_shipping_address_address1").clear()
        driver.find_element_by_id("checkout_shipping_address_address1").send_keys(addresses[i])
        time.sleep(1)
        driver.find_element_by_id("continue_button").click()
        time.sleep(3)
        shipping_page = BeautifulSoup(driver.page_source, 'html.parser')
        cheapest_shipping_price = shipping_page.find_all('span', attrs={'class':'radio__label__accessory'})[0].text.strip()
        print(cheapest_shipping_price)
        #Insert data object directly into MongoDB via isnert_one
        data = {
            'country' : countries[i],
            'price' : cheapest_shipping_price
        }
        result=db.reviews.insert_one(data)

        prev_link = shipping_page.find('a', attrs={'class':'step__footer__previous-link'})
        driver.get(base_url + prev_link.attrs['href'])
        time.sleep(3)
    driver.quit()
    return JsonResponse({'message': 'Successfully!'}, status=status.HTTP_204_NO_CONTENT)
