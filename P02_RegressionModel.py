# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:22:23 2020

@author: Chi Lam
"""


# Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from scipy import stats
from scipy.stats import norm, skew
import statsmodels.api as sm

# Read in data
df = pd.read_csv('housing_data_eda.csv')


# Initiate data splitting STRATIFIED BASED ON 'AREA'
X = df.drop('rent', axis = 1)
y = df.rent.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = df.area)

del X_train['area'] #Only need it to stratify the sample
del X_test['area']


# Test for assumptions
## Normality
### Rent
sns.distplot(y_train, fit = norm, label = 'Samples', fit_kws={"label": "Normal Distribution"}, kde_kws={"label": "Observed estimation"})
plt.legend()
plt.show()

stats.probplot(y_train, plot = plt)
plt.show()

# Grocery
X_train.grocery.min()
X_train.grocery = np.log(X_train.grocery)

print('Skewness of grocery from train df: ', X_train.grocery.skew()) #check for the skewness
print('Kurtosis of grocery from train df: ', X_train.grocery.kurt()) 

## Homoscedasticity
## Linearity
## Absence of correlated errors.

# Regression model
## Multiple linear regression
X_sm = X = sm.add_constant(X)
del X_sm['area']
model = sm.OLS(np.asarray(y), X_sm.astype(float))
model.fit().summary()

reg_linear = LinearRegression()
reg_linear.fit(X_train, y_train)

np.mean(cross_val_score(reg_linear, X_train, y_train, scoring = 'neg_mean_absolute_error'))

## Lasso regression
reg_las = Lasso()
np.mean(cross_val_score(reg_las, X_train, y_train, scoring = 'neg_mean_absolute_error'))

## Random forest regression
reg_randomforest = RandomForestRegressor()
np.mean(cross_val_score(reg_randomforest, X_train, y_train, scoring = 'neg_mean_absolute_error'))

## XGBoost
reg_xgboost = xgb.XGBRegressor()
np.mean(cross_val_score(reg_xgboost, X_train, y_train, scoring = 'neg_mean_absolute_error'))

## GridsearchCV
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}