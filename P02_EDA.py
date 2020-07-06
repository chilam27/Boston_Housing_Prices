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
df.info() # we see that our df has no null value
df.head()


#Univariate Analysis on target variable ('rent') (use the target variable to do the analysis)
df.rent.describe()

plt.figure(figsize=(15, 5))
plt.subplot(121)
sns.distplot(df.rent, fit = norm, label = 'Data', fit_kws={"label": "Normal Distribution"}, kde_kws={"label": "Observed estimation"})
plt.title('Figure 4a: rent distribtuion before log transformation.')
plt.text(19500,0.00039,'Skewness of rent: %s \n Kurtosis of rent: %s' % (round(df.rent.skew(),4),round(df.rent.kurt(),4)),bbox=dict(facecolor='none',edgecolor='black',boxstyle='square'), fontsize=8)
plt.legend()

plt.subplot(122)
sns.distplot(np.log(df.rent), fit = norm, label = 'Data', fit_kws={"label": "Normal Distribution"}, kde_kws={"label": "Observed estimation"})
plt.title('Figure 4b: rent distribtuion after log transformation.')
plt.text(9,1.4,'Skewness of log(rent): %s \n Kurtosis of log(rent): %s' % (round(np.log(df.rent.skew()),4),round(np.log(df.rent.kurt()),4)),bbox=dict(facecolor='none',edgecolor='black',boxstyle='square'), fontsize=8)
plt.legend()
plt.show()

plt.figure(figsize=(13, 5))
plt.subplot(121)
stats.probplot(df.rent, plot = plt)
plt.title('Figure 5a: rent probability plot')

plt.subplot(122)
stats.probplot(np.log(df.rent), plot = plt)
plt.title('Figure 5b: log(rent) probability plot')
plt.show()

df.rent = np.log(df.rent) # for normalization and easy interpretation

##Multivariate analysis (use two or more variables for analysis)
plt.subplots(figsize=(12, 10))
sns.jointplot(df.bed, df.rent, kind='reg')
plt.xlabel('bath \n Figure 6: bedroom vs. rent')

plt.subplots(figsize=(12, 10))
sns.jointplot(df.bath, df.rent, kind='reg')
plt.xlabel('bath \n Figure 7: bathroom vs. rent')


#Remove outliers
##Z-scores
num_var = df.dtypes[df.dtypes != 'object'].index #numerical variables

z_scores = np.abs(stats.zscore(df[num_var]))
print(z_scores)

df = df[(z_scores < 3).all(axis = 1)]
df.reset_index(drop = True, inplace = True)

plt.subplots(figsize=(15, 5))
sns.distplot(df.rent)
plt.title("Figure 8: rent's distribution after removing outliers", fontsize=15)

#Determine variables
##Determine numerical and categorcial variables
cat_var = df.dtypes[df.dtypes == 'object'].index #categorical variables


##Plot heat map
corr = df.corr()
plt.subplots(figsize=(15, 12))
sns.heatmap(corr, vmax = .8, square = True, annot = True, cmap = "Greens")
plt.title('Figure 9: variables correlations heatmap', fontsize=15)


##Other variables skewness and kurtosis
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
plt.title('Figure 11: variables correlations zoomed heatmap', fontsize=15)

num_var_high_corr = ['rent', 'bath', 'bed', 'grocery']

sns.set()
sns.pairplot(df[num_var_high_corr], kind = 'reg', size = 2.5)
plt.suptitle('Figure 12: strong correlation numerical variables pairplot', y=1.03, fontsize=15)
plt.show()


##Categorical, 'area' graph is above
###Creating neighborhoods proportions table
boston = {'neighborhoods' : ['East Boston', 'Charlestown', 'Allston', 'Central', 'Back Bay/ Beacon Hill', 'South Boston', 'South End', 'Fenway', 'Mission Hill', 'Roxbury', 'Dorchester', 'Jamaica Plain', 'Mattapan', 'Roslindale', 'West Roxbury', 'Hyde Park'],
          'percent_area' : [0.103, 0.029, 0.093, 0.024, 0.019, 0.066, 0.023, 0.024, 0.011, 0.082, 0.13, 0.053, 0.061, 0.079, 0.111, 0.094]}

boston_neighborhood = pd.DataFrame(boston, columns= ['neighborhoods','percent_area'])

###Data to plot (credit to Kevin Amipara)
pie_color = ['#E14D43','#a3ca61','#fbcf61','#d97781', '#523e7c', '#428bca', '#D0cc99', '#0d4261', '#f77e05', '#f2b91f', '#94b998', '#ec3939', '#897960', '#2d4f70', '#386665', '#657cc3']

plt.subplots(figsize=(12, 10))
plt.pie(boston_neighborhood['percent_area'], labels = boston_neighborhood['neighborhoods'], colors = pie_color, autopct='%1.1f%%', startangle = 70, pctdistance=0.85)
centre_circle = plt.Circle((0, 0),0.70, fc = 'white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.title("Figure 13: neighborhoods' areas proportion of Boston", fontsize=15)
plt.tight_layout()
plt.show()

plt.subplots(figsize=(25, 9))
sns.boxplot(x = df.area, y = df.rent)
plt.title('Figure 15: area vs. rent boxplot', fontsize=15)


plt.figure(figsize = (12,5))
plt.subplot(121)
sns.boxplot(x = df.property_type, y = df.rent)
plt.title('Figure 16: property type vs. rent boxplot', fontsize=15)

plt.subplot(122)
sns.boxplot(x = df.crime, y = df.rent)
plt.title('Figure 17: crime rate vs. rent boxplot', fontsize=15)
plt.tight_layout()


###Create dummy variables for categorical variables
df_dumies = pd.get_dummies(df, columns=['area', 'property_type', 'crime'])
df_dumies['area'] = df['area']


#Export to CSV
df_dumies.to_csv('housing_data_eda.csv', index = False)