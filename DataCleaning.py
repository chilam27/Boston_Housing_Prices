# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:07:16 2020

@author: theon
"""

#ImportModule
import pandas as pd


#Read data
housing_df = pd.read_csv('boston_data.csv')


#explore
housing_df.columns
housing_df.describe()


#Remove duplicate
housing_df.drop_duplicates(inplace = True)
housing_df.reset_index(drop = True, inplace = True)


#Column values edit
##Rent
housing_df.Rent = housing_df.Rent.apply(lambda x: x.replace('$','')) #remove '$' at the beginning of value
housing_df.Rent = housing_df.Rent.apply(lambda x: x.replace('/mo',''))
housing_df.Rent = housing_df.Rent.apply(lambda x: x.replace(',',''))
housing_df.Rent = housing_df.Rent.apply(lambda x: x.replace(' ',''))

for x in range(len(housing_df.Rent)):
    if '-' in housing_df.Rent[x]:
        a = int(housing_df.Rent[x].split('-')[0])
        b = int(housing_df.Rent[x].split('-')[1])
        housing_df.Rent[x] = (a+b)/ 2


##Area
housing_df.Area.unique().tolist()

for x in range(len(housing_df.Area)):
    housing_df.Area[x] = housing_df.Area[x].split(',')[0]

for x in range(len(housing_df.Area)):
    if 'Allston' in housing_df.Area[x] or "Brighton" in housing_df.Area[x]:
        housing_df.Area[x] = "Allston/ Brighton"
    elif 'North End' in housing_df.Area[x] or 'Downtown' in housing_df.Area[x] or 'Chinatown' in housing_df.Area[x] or 'Haymarket' in housing_df.Area[x] or 'Leather District' in housing_df.Area[x]:
        housing_df.Area[x] = "Central"
    elif 'Dorchester' in housing_df.Area[x]:
        housing_df.Area[x] = "Dorchester"      
    elif 'Fenway' in housing_df.Area[x] or 'Kenmore' in housing_df.Area[x]:
        housing_df.Area[x] = "Fenway Kenmore"
        
housing_df = housing_df[housing_df.Area != 'Boston']
housing_df = housing_df[housing_df.Area != 'Oak Hill']
housing_df = housing_df[housing_df.Area != 'Peabody']
housing_df.reset_index(drop = True, inplace = True)

housing_df.Area.value_counts()


##Bed & bath
housing_df.Bed.value_counts()

for x in range(len(housing_df.Bed)):
    housing_df.Bed[x] = housing_df.Bed[x].split(' ')[0]
    if '-' in housing_df.Bed[x]:
        housing_df.Bed[x] = housing_df.Bed[x].split('-')[1]
        
housing_df.Bath = housing_df.Bath.fillna('0')
for x in range(len(housing_df.Bath)):
    housing_df.Bath[x] = housing_df.Bath[x].split(' ')[0]
    if '-' in housing_df.Bath[x]:
        housing_df.Bath[x] = housing_df.Bath[x].split('-')[1]


##School


##Crime


##Commute


##Shop eat


##Description


##Feature




