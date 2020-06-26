# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:51:09 2020

@author: Chi Lam
"""

#Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split
from scipy import stats
from scipy.stats import norm, skew

#Read in data
train_df = pd.read_csv('train_housing_cleaned.csv')
test_df = pd.read_csv('test_housing_cleaned.csv')


#Explore data
train_df.shape
test_df.shape

train_df.info()
test_df.info() #from '.info()', we see that none of the two df has null value
a
train_df.describe()
test_df.describe()

train_df.head()
test_df.head()


#Analyze 'rent'
train_df.rent.describe()

print('Skewness of rent from train df: ', train_df.rent.skew()) #check for the skewness
print('Kurtosis of rent from train df: ', train_df.rent.kurt()) #check for the pointy-ness

sns.distplot(train_df.rent, fit = norm, label = 'Samples', fit_kws={"label": "Normal Distribution"}, kde_kws={"label": "Observed estimation"})
plt.legend()
plt.show()

stats.probplot(train_df.rent, plot = plt)
plt.show()

##Log-transformation for target variable ('rent')
train_df.rent = np.log(train_df.rent)

print('Skewness of log transformed rent from train df: ', train_df.rent.skew()) #check for the skewness
print('Kurtosis of log transformed rent from train df: ', train_df.rent.kurt()) #check for the pointy-ness

sns.distplot(train_df.rent, fit = norm, label = 'Log Transformed Samples', fit_kws={"label": "Normal Distribution"}, kde_kws={"label": "Observed estimation"})
plt.legend()
plt.show()

stats.probplot(train_df.rent, plot = plt)
plt.show()

#Determine variables
##Creating neighborhoods proportions table
boston = {'neighborhoods' : ['East Boston', 'Charlestown', 'Allston', 'Central', 'Back Bay/ Beacon Hill', 'South Boston', 'South End', 'Fenway', 'Mission Hill', 'Roxbury', 'Dorchester', 'Jamaica Plain', 'Mattapan', 'Roslindale', 'West Roxbury', 'Hyde Park'],
          'percent_area' : [0.103, 0.029, 0.093, 0.024, 0.019, 0.066, 0.023, 0.024, 0.011, 0.082, 0.13, 0.053, 0.061, 0.079, 0.111, 0.094]}

boston_neighborhood = pd.DataFrame(boston, columns= ['neighborhoods','percent_area'])

##Data to plot
pie_color = ['#E14D43','#a3ca61','#fbcf61','#d97781', '#523e7c', '#428bca', '#D0cc99', '#0d4261', '#f77e05', '#f2b91f', '#94b998', '#ec3939', '#897960', '#2d4f70', '#386665', '#657cc3']

plt.pie(boston_neighborhood['percent_area'], labels = boston_neighborhood['neighborhoods'], colors = pie_color, autopct='%1.1f%%', startangle = 70, pctdistance=0.85)
centre_circle = plt.Circle((0, 0),0.70, fc = 'white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.tight_layout()
plt.show()

sns.boxplot(x = train_df.area, y = train_df.rent)


##Determine numerical and categorcial variables
###Transform some numerical variables to categorical
train_df.laundry = train_df.laundry.apply(str)
train_df.ac = train_df.ac.apply(str)
train_df.dishwasher = train_df.dishwasher.apply(str)
train_df.washer = train_df.washer.apply(str)
train_df.dryer = train_df.dryer.apply(str)
train_df.fridge = train_df.fridge.apply(str)
train_df.pet_allowed = train_df.pet_allowed.apply(str)
train_df.parking = train_df.parking.apply(str)



num_var = train_df.dtypes[train_df.dtypes != 'object'].index
print('Numerical variables are: ', num_var)

cat_var = train_df.dtypes[train_df.dtypes == 'object'].index
print('Categorical variables are: ', cat_var)


##Plot heat map
corr = train_df.corr()
plt.subplots(figsize=(12, 9))
sns.heatmap(corr, vmax = .8, square = True, annot = True, cmap = "Greens")


#Remove outliers
##Uni-variate (use the target variable to do the analysis)
sns.boxplot(train_df.rent)

##Multi-variate (use two or more variables for analysis)
sns.jointplot(train_df.bath, train_df.rent)

#Z-scores
z_scores = np.abs(stats.zscore(train_df[num_var]))
print(z_scores)

train_df = train_df[(z_scores < 3).all(axis = 1)]


##Log transform for other variables
for x in num_var:
    print(x, 'Skewness: ', train_df[x].skew(), '  ', 'Kurotsis: ', train_df[x].kurt())


#Determine variables relationships
##Numerical
corr['rent'].sort_values(ascending = False)

sns.set()
num_var_col = ['rent', 'bath', 'bed', 'restaurant', 'nightlife', 'grocery', 'total_amenties']
sns.pairplot(train_df[num_var_col], size = 2.5)
plt.show()

##Categorical
sns.boxplot(x = train_df.property_type, y = train_df.rent)
sns.boxplot(x = train_df.crime, y = train_df.rent)
sns.boxplot(x = train_df.laundry, y = train_df.rent)
sns.boxplot(x = train_df.ac, y = train_df.rent)
sns.boxplot(x = train_df.dishwasher, y = train_df.rent)
sns.boxplot(x = train_df.washer, y = train_df.rent)
sns.boxplot(x = train_df.dryer, y = train_df.rent)
sns.boxplot(x = train_df.fridge, y = train_df.rent)
sns.boxplot(x = train_df.pet_allowed, y = train_df.rent)
sns.boxplot(x = train_df.parking, y = train_df.rent)







