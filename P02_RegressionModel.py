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
from sklearn.metrics import mean_absolute_error
import xgboost as xgb
from scipy import stats
from scipy.stats import norm, skew
import statsmodels.api as sm
import pickle


# Read in data
df = pd.read_csv('housing_data_eda.csv')


# Initiate data splitting STRATIFIED BASED ON 'AREA'
X = df.drop('rent', axis = 1)
y = df.rent.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = df.area, random_state = 1)

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
X_train.grocery.min() #check for '0'
X_train.grocery = np.log(X_train.grocery)

print('Skewness of grocery from train df: ', X_train.grocery.skew()) #check for the skewness
print('Kurtosis of grocery from train df: ', X_train.grocery.kurt()) 

## Homoscedasticity
## Linearity
## Absence of correlated errors.

# Regression model
## Multiple linear regression
X_sm = X = sm.add_constant(X) #create a column of all '1' create an intercept to the slope of the regression line; this is necessary for stats model
del X_sm['area']
model = sm.OLS(np.asarray(y), X_sm.astype(float))
model.fit().summary() #'R-squared: 0.648 = our model explains 64% of variations in Trulia rent

reg_lin = LinearRegression()
reg_lin.fit(X_train, y_train)
np.mean(cross_val_score(reg_lin, X_train, y_train, scoring = 'neg_mean_absolute_error'))

## Lasso regression
alpha = []
error = []

for i in range(1,100):
    alpha.append(i/10)
    regression = Lasso(alpha = (i/10))
    error.append(np.mean(cross_val_score(regression, X_train, y_train, scoring = 'neg_mean_absolute_error')))
    
plt.plot(alpha, error) #plot to see which alpha has the lowest error value

y_max = max(error)
y_max_index = error.index(y_max)
print (y_max, alpha[y_max_index])

reg_las = Lasso(alpha = alpha[y_max_index])
reg_las.fit(X_train, y_train)
np.mean(cross_val_score(reg_las, X_train, y_train, scoring = 'neg_mean_absolute_error'))


## Random forest regression (give the best result, apply 'gridsearchCV')
reg_rf = RandomForestRegressor(random_state = 1)
reg_rf.fit(X_train, y_train)
np.mean(cross_val_score(reg_rf, X_train, y_train, scoring = 'neg_mean_absolute_error'))

## XGBoost
reg_xgboost = xgb.XGBRegressor()
reg_xgboost.fit(X_train, y_train)
np.mean(cross_val_score(reg_xgboost, X_train, y_train, scoring = 'neg_mean_absolute_error'))

## GridsearchCV
parameters = {'n_estimators': range(10,300,10), 'criterion': ('mse', 'mae'), 'max_features': ('auto', 'sqrt', 'log2')}
grid = GridSearchCV(reg_rf, parameters, scoring = 'neg_mean_absolute_error')
grid.fit(X_train, y_train)

grid.best_score_
grid.best_estimator_


#Predict Test set
reg_lin_test = reg_lin.predict(X_test)
reg_las_test = reg_las.predict(X_test)
reg_xgboost_test = reg_xgboost.predict(X_test)
reg_rf_test = grid.best_estimator_.predict(X_test)

mean_absolute_error(y_test, reg_lin_test)
mean_absolute_error(y_test, reg_las_test)
mean_absolute_error(y_test, reg_xgboost_test)
mean_absolute_error(y_test, reg_rf_test) #best one


#Pickle model
pickl = {'model': grid.best_estimator_}
pickle.dump(pickl, open( 'model.pkl', "wb")) 

file_name = "model.pkl"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0]

list(X_test.iloc[1,:])
