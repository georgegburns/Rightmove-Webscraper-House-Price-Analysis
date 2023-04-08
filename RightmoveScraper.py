import os
import time
from datetime import date

import bs4 as bs
import pandas as pd
import requests
from RightmoveDictionary import AREA_CODES
from RightmoveSupportFunctions import locationSearch

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
TODAY = date.today()
TOSCRAPE = list(AREA_CODES.values())

def RightmoveScraper(area=TOSCRAPE, buy_type='all', df=None):
    
    buy_types = ['all', 'rent', 'buy']
    if buy_type not in buy_types:
        raise ValueError("Invalid variable. Expected one of: %s" % buy_types)
    
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 'Accept-Enconding' : 'grip, deflate', 'Accept' : '*/*', 'Connection' : 'keep-alive'}
    URL = 'https://www.rightmove.co.uk/'
    RENT = 'property-to-rent/'
    BUY = 'property-for-sale/'
    TAIL = 'find?locationIdentifier=OUTCODE%5E'
    SORT = '&sortType=6'
    PER_PAGE = '&index='
    RENT_BUY = buy_type
    LOCATION = 'UK'
    Scraping = True
    
    nums = area
    if area != TOSCRAPE:
        HELPER = locationSearch(area)
        nums = HELPER[0]
        LOCATION = HELPER[1]
        if nums == None:
            print(f"Location can't be found, the function can only work with Area Codes, Towns, Countys and UK Regions. Ensure value is a string. Your input was {area}")
            Scraping = False
    
    i = 0
    page_num = 1
    index = 0
    label = 'Rent'

    AREAS = []
    PRICES = []
    HOUSES = []
    TYPES = []
    DATES = []
    WEBPAGES = []

    print(f'Scraping properties in {LOCATION}')
    
    while Scraping:
        LENGTH = len(nums)

        if LENGTH > 0:
            num = nums[i]
        else:
            Scraping = False
            
        UNAVAILABLE = False
        
        PAGE = URL + RENT + TAIL + str(num) + SORT + PER_PAGE + str(index)
        if 'buy' in RENT_BUY:
            label = 'Buy'
            PAGE = URL + BUY + TAIL + str(num) + SORT + PER_PAGE + str(index)

        URLPAGE = requests.get(PAGE, headers=HEADERS, timeout=10)
        HTML = URLPAGE.content
        SOUP = bs.BeautifulSoup(HTML, 'html.parser')
        
        AREA = SOUP.find('h1', class_='searchTitle-heading').text.split()[4]
        time.sleep(0.05)
        PROPERTIES = SOUP.find_all('div', class_='propertyCard-wrapper')
        if PROPERTIES in WEBPAGES:
            UNAVAILABLE = True
            
        WEBPAGES.append(PROPERTIES)
        
        print(f'Scraping page {page_num} of {label} properties in {AREA}')
        
        for j in range(len(PROPERTIES)):
            
            try:
                PRICE = SOUP.find_all('span', class_='propertyCard-priceValue')[j].text.strip()
            except:
                PRICE = SOUP.find_all('div', class_='propertyCard-priceValue')[j].text.strip()
                
            if not PRICE:
                break
            
            HOUSE = SOUP.find_all('h2', class_='propertyCard-title')[j].text.strip('\\n').strip()
            DATE = SOUP.find_all('span', class_='propertyCard-branchSummary-addedOrReduced')[j].text.strip()
            
            PRICES.append(PRICE)
            AREAS.append(AREA)
            HOUSES.append(HOUSE)
            DATES.append(DATE)
            TYPES.append(label)
                
        if i == LENGTH or page_num == 41:
            UNAVAILABLE = True
                
        if UNAVAILABLE:
            page_num = 0
            i += 1
            WEBPAGES = []
            if i == LENGTH:
                if 'all' not in RENT_BUY:
                    Scraping = False
                RENT_BUY = 'buy'
                i = 0
            index = 0
            UNAVAILABLE = False
        page_num += 1
        index += 24

        
    COLUMNS = ('Area Code', 'Price', 'House Type', 'Payment Type', 'Date Added/Reduced')
    TEMP = list(zip(AREAS, PRICES, HOUSES, TYPES, DATES))
    TEMP = pd.DataFrame(TEMP,columns=COLUMNS)
    if df:
        OUTPUT = pd.read_excel(DESKTOP + f'/Rightmove Listings - {LOCATION} - {TODAY}.xlsx')
        OUTPUT = pd.concat([TEMP,OUTPUT], axis=0)
        OUTPUT.to_excel(DESKTOP + f'/Rightmove Listings - {LOCATION} - {TODAY}.xlsx', index=False)
    else:
        TEMP.to_excel(DESKTOP + f'/Rightmove Listings - {LOCATION} - {TODAY}.xlsx', index=False)
        


