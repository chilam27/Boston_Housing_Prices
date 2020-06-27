# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:22:23 2020

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
df = pd.read_csv('housing_data_eda.csv')


#Initiate data splitting STRATIFIED BASED ON 'AREA'
X = df.drop('rent', axis = 1)
y = df.rent.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = df.area)


#Test for assumptions
##Normality
###Rent
sns.distplot(y_train, fit = norm, label = 'Samples', fit_kws={"label": "Normal Distribution"}, kde_kws={"label": "Observed estimation"})
plt.legend()
plt.show()

stats.probplot(y_train, plot = plt)
plt.show()

print('Skewness of rent from train df: ', y_train.skew()) #check for the skewness
print('Kurtosis of rent from train df: ', y_train.kurt()) #check for the pointy-ness

###Restaurant
X_train.restaurant.min()
X_train.restaurant = np.log(X_train.restaurant)

print('Skewness of rent from train df: ', X_train.restaurant.skew()) #check for the skewness
print('Kurtosis of rent from train df: ', X_train.restaurant.kurt()) #check for the pointy-ness

#Nightlife
X_train.nightlife.min() #because it has zero (cannot do log with zero), we need to create a new column

X_train['HasNightlife'] = pd.Series(len(X_train['nightlife']), index = X_train.index)
X_train['HasNightlife'] = 0 
X_train.loc[X_train['nightlife']>0,'HasNightlife'] = 1

X_train.loc[X_train['HasNightlife']==1,'nightlife'] = np.log(X_train['nightlife'])

print('Skewness of rent from train df: ', X_train.nightlife.skew()) #check for the skewness
print('Kurtosis of rent from train df: ', X_train.nightlife.kurt()) #check for the pointy-ness

#Grocery
X_train.grocery.min()
X_train.grocery = np.log(X_train.grocery)

print('Skewness of rent from train df: ', X_train.grocery.skew()) #check for the skewness
print('Kurtosis of rent from train df: ', X_train.grocery.kurt()) 

##Homoscedasticity