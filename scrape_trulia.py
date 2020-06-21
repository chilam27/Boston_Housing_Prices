# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:13:26 2020

@author: Karishma Parashar
@url: https://github.com/Abmun/WebScraping-RentalProperties
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
# sugg_income = []
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
    while(count < 6):  #will go till 5 pages = 150 records
        req = Request(x, headers=get_headers())  #req all headers
        htmlfile = urlopen(req)
        htmltext = htmlfile.read()
        #print (htmltext)
        soup = BS(htmltext,'html.parser')
        #print (soup.prettify())
        
        for tag in soup.find_all('div',attrs={'data-testid' : 'pagination-caption'}):
                result = tag.get_text(strip = True) #save number of results for the search
        result= result.split(' ')[2]
        result= int(result.replace(',',''))
       
        for tag in soup.find_all('div',attrs={'data-testid' : 'property-price'}): #rent
                row = tag.get_text(strip = True)
                if not row:
                    row = "NA"
                print(row)
                rent.append(row)

        for tag in soup.find_all('div',attrs={'data-testid' : 'property-street'}): #address
                row = tag.get_text(strip = True)
                if not row:
                    row = "NA"
                print(row)
                address.append(row)             
        
        for tag in soup.find_all('div',attrs={'data-testid' : 'property-region'}): #area
                row = tag.get_text(strip = True)
                if not row:
                    row = "NA"
                print(row)
                area.append(row)
                
                
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
                for tag2 in tag.find_all('li', attrs= {'data-testid': 'bed'}):
                    row= tag2.get_text(strip = True)
                    if not 'Bed' in row:
                        row= "NA"
                bed.append(row)     
                
                for tag2 in tag.find_all('li', attrs = {'data-testid': 'bath'}):
                    row= tag2.get_text(strip= True)
                    if not 'Bath' in row:
                        row= "NA"
                bath.append(row)
           
            for tag in soup.find_all('div',attrs= {'aria-label': 'Schools'}):  #school
                row= tag.get_text(strip = True)
                if not row:
                    row= "NA"
                print(row)
                school.append(row)           
            
            for tag in soup.find_all('div',attrs= {'aria-label': 'Crime'}):  #crime
                row= tag.get_text(strip = True)
                if not row:
                    row= "NA"
                print(row)
                crime_rate.append(row)
               
            for tag in soup.find_all('div',attrs= {'aria-label': 'Commute'}): #commute
                row= tag.get_text(strip = True)
                if not row:
                    row= "NA"
                print(row)
                commute.append(row)
                
            for tag in soup.find_all('div', attrs= {'aria-label': 'Shop & Eat'}): #shop and eat
                row= tag.get_text(strip = True)
                if not row:
                    row= "NA"
                print(row)
                shop_eat.append(row)
            
            # for tag in soup.find_all('div', attrs= {'class': 'HomeDetailsRentalAffordability__IncomeInformationContainer-epkvqi-0 jalLqQ'}):
            #     for tag2 in tag.find_all('span', attrs= {'class': 'Text__TextBase-sc-1i9uasc-0 dltAqT'}): #suggested income
            #         row= tag2.get_text(strip = True)    
            #         if not '$' in row:   
            #             row= "NA"
            #         sugg_income.append(row)
             
            for tag in soup.find_all('div',attrs= {'data-testid': 'seo-description-paragraph'}): #descp
                row= tag.get_text(strip = True)
                if not row:
                    row= "NA"
                print(row)
                descp.append(row)
                
            for tag in soup.find_all('div',attrs= {'data-testid': 'features-container'}): #feature
                    row= tag.get_text(strip= True)
                    if not row:
                        row= "NA"
                    print(row)
                    feature.append(row)

             
        count= count+1
        page= str(count)+ "_p"  #changes page
        x= y+ page
        
        if result <= len(area): #stop loop from repetting itself
            break

        
data_frame = pd.DataFrame(list(zip(rent, address, area, bed, bath, school, crime_rate, commute, shop_eat, descp, feature, addr_link)), columns = ["Rent", "Address", "Area", "Bed", "Bath", "School", "Crime", "Commute", "Shop_eat", "Description", "Feature", "URL"])
data_frame

#Save the obtained dataframe to csv
#data_frame.to_csv('Newton_data.csv')
