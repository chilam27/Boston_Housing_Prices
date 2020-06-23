# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:13:26 2020

@author: theon
@acknowledgement: https://github.com/Abmun/WebScraping-RentalProperties
"""

from urllib.request import urlopen,Request
from bs4 import BeautifulSoup as BS
import urllib.request
import urllib.parse
import urllib.error
import ssl
import re
import pandas as pd


def get_headers():
    headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language':'en-US,en;q=0.9',
            'cache-control':'max-age=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    return headers


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

rent = []
address = []
area = []
bed = []
bath = []
school = []
crime_rate = []
commute = []
shop_eat = []
sugg_income = []
descp = []
feature = []
addr_link = []

urls = ["https://www.trulia.com/for_rent/02128_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02129_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02134_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02109_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02111_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02108_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02115_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02127_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02118_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02215_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02120_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02119_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02122_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02130_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02126_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02131_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02132_zip/1p_beds/",
        "https://www.trulia.com/for_rent/02136_zip/1p_beds/"]


for x in urls:
    count = 1
    y = x
    print(x)
    while(count < 6):  #will go till 5 pages = 150 records
        req = Request(x, headers=get_headers())  #req all headers
        htmlfile = urlopen(req)
        htmltext = htmlfile.read()
        #print (htmltext)
        soup = BS(htmltext,'html.parser')
        #print (soup.prettify())
        
        for tag in soup.find_all('div',attrs={'data-testid' : 'pagination-caption'}):
                result = tag.get_text(strip = True) #save number of results for the search
        try:
            result= result.split(' ')[2]
            result= int(result.replace(',',''))
        except:
            pass
       
        for tag in soup.find_all('div',attrs={'data-testid' : 'property-price'}): #rent
                rent_record = "NA"        
                rent_record = tag.get_text(strip = True)
                if not rent_record:
                    rent_record = "NA"
                # print(rent_record)
                rent.append(rent_record)

        for tag in soup.find_all('div',attrs={'data-testid' : 'property-street'}): #address
                address_record = "NA"
                address_record = tag.get_text(strip = True)
                if not address_record:
                    address_record = "NA"
                # print(address_record)
                address.append(address_record)             
        
        for tag in soup.find_all('div',attrs={'data-testid' : 'property-region'}): #area
                area_record = "NA"
                area_record = tag.get_text(strip = True)
                if not area_record:
                    area_record = "NA"
                # print(area_record)
                area.append(area_record)
                
                
        links = []                                   
        for cards in soup.find_all('div',attrs={'class':'PropertyCard__PropertyCardContainer-sc-1ush98q-2'}):       
            
            for link in cards.findAll('a', attrs={'href': re.compile("^/")}):\
                links.append("https://www.trulia.com" + link.get('href')) #appends all links in the page
       
        #print(links) #picking up each link and reading inside it
        for link in links:
            addr_link.append(link)
            req = Request(link, headers=get_headers())
            htmlfile = urlopen(req)
            htmltext = htmlfile.read()
            #print (htmltext)
            soup = BS(htmltext,'html.parser')  #reads inside links
            #print("hello")
           
            for tag in soup.find_all('div', attrs= {'class': 'Grid__CellBox-sc-5ig2n4-0 fxOuBE'}):
                bed_record = "NA"
                bath_record = "NA"
                for tag2 in tag.find_all('li', attrs= {'data-testid': 'bed'}):
                    bed_record = tag2.get_text(strip = True)
                    if not 'Bed' in bed_record:
                        bed_record= "NA"
                bed.append(bed_record)     
                
                for tag2 in tag.find_all('li', attrs = {'data-testid': 'bath'}):
                    bath_record = tag2.get_text(strip= True)
                    if not 'Bath' in bath_record:
                        bath_record= "NA"
                bath.append(bath_record)
           
            for tag in soup.find_all('div',attrs= {'aria-label': 'Schools'}):  #school
                school_record = "NA"
                school_record = tag.get_text(strip = True)
                if not school_record:
                    school_record= "NA"
                # print(school_record)
                school.append(school_record)           
            
            for tag in soup.find_all('div',attrs= {'aria-label': 'Crime'}):  #crime
                crime_record = "NA"
                crime_record = tag.get_text(strip = True)
                if not crime_record:
                    crime_record= "NA"
                # print(crime_record)
                crime_rate.append(crime_record)
               
            for tag in soup.find_all('div',attrs= {'aria-label': 'Commute'}): #commute
                commute_record = "NA"
                commute_record = tag.get_text(strip = True)
                if not commute_record:
                    commute_record= "NA"
                # print(commute_record)
                commute.append(commute_record)
                
            for tag in soup.find_all('div', attrs= {'aria-label': 'Shop & Eat'}): #shop and eat
                shopeat_record = "NA"
                shopeat_record = tag.get_text(strip = True)
                if not shopeat_record:
                    shopeat_record = "NA"
                # print(shopeat_record)
                shop_eat.append(shopeat_record)
            
            for tag in soup.find_all('div', attrs= {'class': 'HomeDetailsRentalAffordability__IncomeInformationContainer-epkvqi-0 jalLqQ'}):
                income_record = "NA"
                for tag2 in tag.find_all('span', attrs= {'class': 'Text__TextBase-sc-1i9uasc-0 dltAqT'}): #suggested income
                    income_record = tag2.get_text(strip = True)    
                    if not '$' in income_record:   
                        income_record = "NA"
                sugg_income.append(income_record)
             
            for tag in soup.find_all('div',attrs= {'data-testid': 'seo-description-paragraph'}): #descp
                descp_record = "NA"
                descp_record = tag.get_text(strip = True)
                if not descp_record:
                    descp_record = "NA"
                # print(descp_record)
                descp.append(descp_record)
                
            for tag in soup.find_all('div',attrs= {'data-testid': 'features-container'}): #feature
                feature_record = "NA"        
                feature_record = tag.get_text(strip= True)
                if not feature_record:
                    feature_record = "NA"
                # print(feature_record)
                feature.append(feature_record)

             
        count= count+1
        page= str(count)+ "_p"  #changes page
        x= y+ page
        
        if result <= len(area): #stop loop from repetting itself
            break

        
data_frame = pd.DataFrame(list(zip(rent, address, area, bed, bath, school, crime_rate, commute, shop_eat, descp, feature, addr_link)), columns = ["Rent", "Address", "Area", "Bed", "Bath", "School", "Crime", "Commute", "Shop_eat", "Description", "Feature", "URL"])
data_frame

#Save the obtained dataframe to csv
data_frame.to_csv('boston_data.csv', index = False)