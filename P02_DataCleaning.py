# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:07:16 2020

@author: theon
"""

#ImportModule
import pandas as pd


#Read data
housing_df = pd.read_csv('housing_data_scraped.csv')


#Explore
housing_df.columns
housing_df.describe()
housing_df.isnull().sum() / housing_df.shape[0] #'Bed' and 'Bath' variable are the only two that has null


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
for x in range(len(housing_df.Area)):
    housing_df.Area[x] = housing_df.Area[x].split(',')[0]

for x in range(len(housing_df.Area)):
    if 'North End' in housing_df.Area[x] or 'Downtown' in housing_df.Area[x] or 'Chinatown' in housing_df.Area[x] or 'West End' in housing_df.Area[x]:
        housing_df.Area[x] = "Central"
    elif 'Dorchester' in housing_df.Area[x]:
        housing_df.Area[x] = "Dorchester"      
    elif 'Beacon Hill' in housing_df.Area[x] or "Back Bay" in housing_df.Area[x]:
        housing_df.Area[x] = "Back Bay/ Beacon Hill"

housing_df.Area.value_counts()


##Bed & bath
housing_df.Bed.value_counts()
housing_df.Bath.value_counts()

housing_df.Bed = housing_df.Bed.fillna('0')
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
housing_df.School = housing_df.School.apply(lambda x: x.replace('Schools',''))
housing_df.School = housing_df.School.apply(lambda x: x.replace('School',''))

elementary_school = []
middle_school = []
high_school = []

for x in range(len(housing_df.School)):
    elementary = 0
    middle = 0
    high = 0
    
    if 'Elementary' in housing_df.School[x]:
        elementary = housing_df.School[x].split(' ')[0]
    if 'Middle' in housing_df.School[x]:
        if housing_df.School[x].find('Middle') < 5:
            middle = housing_df.School[x].split(' ')[0]
        else:
            middle = housing_df.School[x].split(' ')[2]
    if 'High' in housing_df.School[x]:
        if housing_df.School[x].find('High') < 5:
            high = housing_df.School[x].split(' ')[0]
        elif housing_df.School[x].find('High') > 10 & housing_df.School[x].find('High') < 16:
            high = housing_df.School[x].split(' ')[2]
        else:
            high = housing_df.School[x].split(' ')[4]
    
    elementary_school.append(int(elementary))
    middle_school.append(int(middle))
    high_school.append(int(high))
    
housing_df['elemenatary_school'] = elementary_school
housing_df['middle_school'] = middle_school
housing_df['high_school'] = high_school

housing_df.School = housing_df.elemenatary_school + housing_df.middle_school + housing_df.high_school


##Crime
housing_df.Crime = housing_df.Crime.apply(lambda x: x.replace('Crime',''))
housing_df.Crime = housing_df.Crime.apply(lambda x: x.split(' ')[0])


##Commute
housing_df.Commute = housing_df.Commute.apply(lambda x: x.replace('Commute',''))
housing_df.Commute = housing_df.Commute.apply(lambda x: x.split(' ')[0])
housing_df.Commute = housing_df.Commute.apply(lambda x: x.replace('%',''))
housing_df.Commute = housing_df.Commute.apply(lambda x: x.replace("Learn",'0'))
housing_df = housing_df.rename(columns={'Commute': 'car_commute_percent'})


##Shop eat
housing_df.Shop_eat = housing_df.Shop_eat.apply(lambda x: x.replace('Shop & Eat', ''))
housing_df.Shop_eat = housing_df.Shop_eat.apply(lambda x: x.replace('Restaurants', 'res '))
housing_df.Shop_eat = housing_df.Shop_eat.apply(lambda x: x.replace('Groceries', 'gro '))

restaurant = []
grocery = []
nightlife = []

for x in range(len(housing_df.Shop_eat)):
    restaurant.append(int(housing_df.Shop_eat[x].split(' ')[0]))
    grocery.append(int(housing_df.Shop_eat[x].split(' ')[2]))
    if 'Nightlife' in housing_df.Shop_eat[x]:
        nightlife.append(int(housing_df.Shop_eat[x].split(' ')[4]))
    else:
        nightlife.append(0)
    
housing_df['restaurant'] = restaurant
housing_df['grocery'] = grocery
housing_df['nightlife'] = nightlife

del housing_df['Shop_eat']


##Feature
property_type = []
pet_allowed = []
laundry = []
parking = []
ac = []
dishwasher = []
washer = []
dryer = []
fridge = []
total_amenties = []

for x in range(len(housing_df.Feature)):
    prop = ''
    pet = 0
    laun = 0
    park = 0
    ac_num = 0
    dish = 0
    wash = 0
    dry = 0
    frid = 0
    
    if "Multi Family" in housing_df.Feature[x]:
        prop = 'multifamily'
    if "Apartment" in housing_df.Feature[x]:
        prop = 'apartment'
    if "Townhouse" in housing_df.Feature[x]:
        prop = 'townhouse'
    if "Condo" in housing_df.Feature[x]:
        prop = 'condo'
    if "Single Family" in housing_df.Feature[x]:
        prop = 'singlefamily'
    if "allowed" in housing_df.Feature[x]:
        if "No pets Allowed" in housing_df.Feature[x]:
            pet = 0
        else:
            pet = 1
    if "Laundry" in housing_df.Feature[x]:
        laun = 1
    if "Parking" in housing_df.Feature[x]:
        if "Parking Type: none" in housing_df.Feature[x]:
            park = 0
        else:
            park = 1
    if "Air Conditioning" in housing_df.Feature[x]:
        if "No Air Conditioning" in housing_df.Feature[x]:
            ac_num = 0
        else:
            ac_num = 1
    if "Dishwasher" in housing_df.Feature[x]:
        dish = 1
    if "Washer" in housing_df.Feature[x]:
        wash = 1
    if "Dryer" in housing_df.Feature[x]:
        dry = 1
    if "Refrigerator" in housing_df.Feature[x]:
        frid = 1
        
    property_type.append(prop)
    pet_allowed.append(pet)
    laundry.append(laun)
    parking.append(park)
    ac.append(ac_num)
    dishwasher.append(dish)
    washer.append(wash)
    dryer.append(dry)
    fridge.append(frid)
    
housing_df['property_type'] = property_type
housing_df['pet_allowed'] = pet_allowed
housing_df['laundry'] = laundry
housing_df['parking'] = parking
housing_df['ac'] = ac
housing_df['dishwasher'] = dishwasher
housing_df['washer'] = washer
housing_df['dryer'] = dryer
housing_df['fridge'] = fridge

housing_df.Feature = housing_df.laundry + housing_df.ac + housing_df.dishwasher + housing_df.washer + housing_df.dryer + housing_df.fridge
housing_df = housing_df.rename(columns={'Feature': 'total_amenties'})


#Minor fixes to dataframe
housing_df.Rent = housing_df.Rent.astype(int)
housing_df.Bed = housing_df.Bed.astype(float)
housing_df.Bath = housing_df.Bath.astype(float)
housing_df.car_commute_percent = housing_df.car_commute_percent.astype(int)
housing_df.pet_allowed = housing_df.pet_allowed.astype(int)
housing_df.laundry = housing_df.laundry.astype(int)


housing_df = housing_df.rename(columns={'Rent': 'rent', 'Address': 'address', 'Area': 'area', 'Bed': 'bed', 'Bath': 'bath', 'School': 'school', 'Crime': 'crime', 'URL': 'url'}) #change all column names to lowercase
del housing_df['Description'] #'description' is only the summary of other data we have: not useful
del housing_df['address'] #we don't need this piece of info
del housing_df['url']


#Rearrange columns
housing_df.columns.tolist()
housing_df = housing_df[['rent', 'area', 'property_type', 'bed', 'bath', 'school', 'elemenatary_school', 'middle_school', 'high_school', 'crime', 'car_commute_percent', 'total_amenties', 'laundry', 'ac', 'dishwasher', 'washer', 'dryer', 'fridge', 'pet_allowed', 'parking', 'restaurant', 'grocery', 'nightlife']]


#Creating proportion table
# boston = {'neighborhoods' : ['East Boston', 'Charlestown', 'Allston', 'Central', 'Back Bay/ Beacon Hill', 'South Boston', 'South End', 'Fenway', 'Mission Hill', 'Roxbury', 'Dorchester', 'Jamaica Plain', 'Mattapan', 'Roslindale', 'West Roxbury', 'Hyde Park'],
#           'percent_area' : [0.103, 0.029, 0.093, 0.024, 0.019, 0.066, 0.023, 0.024, 0.011, 0.082, 0.13, 0.053, 0.061, 0.079, 0.111, 0.094]
#           }

# boston_neighborhood = pd.DataFrame(boston, columns= ['neighborhoods','percent_area'])


#Deciding sample size = 760
# stratified_sample = pd.DataFrame()
# for x in range(len(boston_neighborhood.neighborhoods)):
#     sub_df = housing_df[housing_df.area == boston_neighborhood.neighborhoods[x]]
#     sub_df = sub_df.sample(n = int(round(760 * boston_neighborhood.percent_area[x], 0)))
#     stratified_sample = pd.concat([stratified_sample, sub_df], ignore_index=True)
    
# stratified_sample.area.value_counts() / stratified_sample.shape[0]

# sns.distplot(stratified_sample.rent)

# sns.boxplot(x = stratified_sample.area, y = stratified_sample.rent)


#Export dataframe to csv
housing_df.to_csv('housing_data_cleaned.csv', index = False)

