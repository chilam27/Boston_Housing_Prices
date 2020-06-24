# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:51:09 2020

@author: Chi Lam
"""

#Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split

#Read in data
housing_df = pd.read_csv('housing_cleaned.csv')
housing_df.info()


#Creating porportion table
boston = {'neighborhoods' : ['East Boston', 'Charlestown', 'Allston/ Brighton', 'Central', 'Beacon Hill', 'Back Bay', 'South Boston', 'South End', 'Fenway Kenmore', 'Mission Hill', 'Roxbury', 'Dorchester', 'Jamaica Plain', 'Mattapan', 'Roslindale', 'West Roxbury', 'Hyde Park'],
          'percent_area' : [0.103, 0.029, 0.093, 0.024, 0.007, 0.012, 0.066, 0.023, 0.024, 0.011, 0.082, 0.13, 0.053, 0.061, 0.079, 0.111, 0.094]
          }

boston_neighborhood = pd.DataFrame(boston, columns= ['neighborhoods','percent_area'])


#Deciding sample size = 508
stratified_sample = pd.DataFrame()
for x in range(len(boston_neighborhood.neighborhoods)):
    sub_df = housing_df[housing_df.area == boston_neighborhood.neighborhoods[x]]
    sub_df = sub_df.sample(n = int(round(508 * boston_neighborhood.percent_area[x], 0)))
    stratified_sample = pd.concat([stratified_sample, sub_df], ignore_index=True)


# Data to plot
pie_color = ['#E14D43','#a3ca61','#fbcf61','#d97781', '#523e7c', '#428bca', '#D0cc99', '#0d4261', '#f77e05', '#f2b91f', '#94b998', '#ec3939', '#897960', '#2d4f70', '#386665', '#657cc3', '#363b3f']

plt.pie(boston_neighborhood['percent_area'], labels = boston_neighborhood['neighborhoods'], colors = pie_color, autopct='%1.1f%%', startangle = 70, pctdistance=0.85)
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.tight_layout()
plt.show()


#Create a bias free testset
sns.distplot(housing_df.rent)
plt.show()

##Plot heat map
corr = housing_df.corr()
plt.subplots(figsize=(12, 9))
sns.heatmap(corr, vmax=.8, square=True, annot = True, cmap="Greens")

##Find correlations
corr['rent'].sort_values(ascending = False)





