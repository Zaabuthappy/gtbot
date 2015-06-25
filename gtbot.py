#!/usr/bin/env python

import requests
import re
import time

baseURL = 'http://www.dealwithitsf.bigcartel.com'
cartURL = baseURL + '/cart'

products = [
    {
        "name"       : "Unicorn",
        "productURL" : baseURL + '/product/unicorn',
        "count"      : 3
    },

    {
        "name"       : "Glossed Walnut Barebones",
        "productURL" : baseURL + '/product/glossed-walnut-barebones',
        "count"      : 2
    }
]

cookie = dict(_big_cartel_session='BAh7BzoNb3JkZXJfaWQiEDExODA1MjIxMjk2Og9zZXNzaW9uX2lkIiVjNjkzMjkxZDkxNzEzYWJhNzcyNzNmYTM4NWMxZDYyYg%3D%3D--03817ed3789da70d2939925659a9153f280df8f9', path='/')

def get_item(productURL, cartURL, cookies):
    itemId = 0
    r = requests.get(productURL, cookies=cookies)
    r.raise_for_status()
    
    for line in r.text.splitlines():
        if line.find('cart[add][id]') != -1:
            match = re.search('value="(\d+)"', line)
            if match:
                itemId = match.group(1);

    if itemId:
        print 'Adding item ' + itemId + ' to cart'
        payload = {'cart[add][id]' : itemId}
        r = requests.post(cartURL, data=payload, cookies=cookies)
        r.raise_for_status()
        return check_errors(r.text)
    
def check_errors(resp_text):
    """
    Returns False if there was an error adding item to cart
    otherwise returns True
    """
    for line in resp_text.splitlines():
        if line.find('Sorry') != -1:
            return False
    return True

for product in products:
    product['current_count'] = 0

products_done = 0
while True:
    for product in products:
        if product['current_count'] < product['count']:
            print product['name'] + ': ', product['current_count'], '/', product['count']
            if get_item(product['productURL'], cartURL, cookie):
                print 'Snagged a ' + product['name']
                product['current_count'] += 1
                if product['current_count'] == product['count']:
                    print 'product done: ' + product['name']
                    products_done += 1

    print "poducts_done: ", products_done
    print "len(products)", len(products)
    if products_done == len(products):
        break
    time.sleep(5)



#if get_item(product, cart, cookie):
#    print 'success'
#else:
#    print 'failed'


