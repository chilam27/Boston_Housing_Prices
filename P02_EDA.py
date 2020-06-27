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
df = pd.read_csv('housing_data_cleaned.csv')


#Explore data
df.shape
df.info() #from '.info()', we see that none of the two df has null value
df.describe()
df.head()


#Analyze 'rent'
df.rent.describe()

print('Skewness of rent from train df: ', df.rent.skew()) #check for the skewness
print('Kurtosis of rent from train df: ', df.rent.kurt()) #check for the pointy-ness

sns.distplot(df.rent, fit = norm, label = 'Samples', fit_kws={"label": "Normal Distribution"}, kde_kws={"label": "Observed estimation"})
plt.legend()
plt.show()

stats.probplot(df.rent, plot = plt)
plt.show()

#Determine variables
##Creating neighborhoods proportions table
boston = {'neighborhoods' : ['East Boston', 'Charlestown', 'Allston', 'Central', 'Back Bay/ Beacon Hill', 'South Boston', 'South End', 'Fenway', 'Mission Hill', 'Roxbury', 'Dorchester', 'Jamaica Plain', 'Mattapan', 'Roslindale', 'West Roxbury', 'Hyde Park'],
          'percent_area' : [0.103, 0.029, 0.093, 0.024, 0.019, 0.066, 0.023, 0.024, 0.011, 0.082, 0.13, 0.053, 0.061, 0.079, 0.111, 0.094]}

boston_neighborhood = pd.DataFrame(boston, columns= ['neighborhoods','percent_area'])

##Data to plot
pie_color = ['#E14D43','#a3ca61','#fbcf61','#d97781', '#523e7c', '#428bca', '#D0cc99', '#0d4261', '#f77e05', '#f2b91f', '#94b998', '#ec3939', '#897960', '#2d4f70', '#386665', '#657cc3']

plt.subplots(figsize=(12, 9))
plt.pie(boston_neighborhood['percent_area'], labels = boston_neighborhood['neighborhoods'], colors = pie_color, autopct='%1.1f%%', startangle = 70, pctdistance=0.85)
centre_circle = plt.Circle((0, 0),0.70, fc = 'white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.tight_layout()
plt.show()

plt.subplots(figsize=(25, 9))
sns.boxplot(x = df.area, y = df.rent)


##Determine numerical and categorcial variables
###Transform some numerical variables to categorical
num_var = df.dtypes[df.dtypes != 'object'].index
print(num_var)

cat_var = df.dtypes[df.dtypes == 'object'].index
print(cat_var)


##Plot heat map
corr = df.corr()
plt.subplots(figsize=(12, 9))
sns.heatmap(corr, vmax = .8, square = True, annot = True, cmap = "Greens")


#Remove outliers
##Uni-variate (use the target variable to do the analysis)
sns.boxplot(df.rent)

##Multi-variate (use two or more variables for analysis)
sns.jointplot(df.bath, df.rent)

##Z-scores
z_scores = np.abs(stats.zscore(df[num_var]))
print(z_scores)

df = df[(z_scores < 3).all(axis = 1)]
df.reset_index(drop = True, inplace = True)


##Log transform for other variables
for x in num_var:
    print(x, 'Skewness: ', df[x].skew(), '  ', 'Kurotsis: ', df[x].kurt()) #we can see that 'restuarant'  has the highest skewness and kurtosis; 'nightlife' also but it has zero values


#Determine variables relationships
##Numerical
corr['rent'].sort_values(ascending = False)

num_var_high_corr = ['rent', 'bath', 'bed', 'restaurant', 'nightlife', 'grocery']

###Zoomed heatmap
corr = df[num_var_high_corr].corr()
sns.set(font_scale = 1.25)
plt.subplots(figsize=(12, 9))
heatmap = sns.heatmap(corr, vmax = .8, square = True, annot = True, cmap = "Greens")
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=30) #we will drop 'restaurant' and 'nightlife' since the two and grocery are highly correlated toward each other and have about the same corr with rent; grocery has higher corr compare to the other two

num_var_high_corr = ['rent', 'bath', 'bed', 'grocery']

sns.set()
sns.pairplot(df[num_var_high_corr], kind = 'reg', size = 2.5)
plt.show()

df_num = df[num_var_high_corr]

##Categorical, 'area' graph is above
plt.figure(figsize = (10,4))

plt.subplot(121)
sns.boxplot(x = df.property_type, y = df.rent)

plt.subplot(122)
sns.boxplot(x = df.crime, y = df.rent)
plt.tight_layout()

df1 = pd.concat([df_num, df[['area', 'property_type', 'crime']]], axis = 1, sort=False)

###Create dummy variables for categorical variables
df_dumies = pd.get_dummies(df1, columns=['area', 'property_type', 'crime'])
df_dumies['area'] = df1['area']


#Export to CSV
df_dumies.to_csv('housing_data_eda.csv', index = False)