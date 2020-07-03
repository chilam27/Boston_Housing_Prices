# Predict Boston Housing Prices

Analyzing and predict Boston housing prices using data scraped from trulia.com using advanced regression models. I will go in depth for all the processes of this project: using `Beautiful Soup` to scrape data, analyzing and comparing different regression models, and building an Application Programming Interface (API) using `Flask`.

## Background and Motivation

My goal for this project is to use the best regression model to predict Boston housing prices on Trulia based on the number of features that the source provides. By the end of the project, I am hoping to be able to answer these questions:
* What are the features that have high effect on to the rent of a property? Does the _neighborhood_ of the property has any effect?
* How good is our prediction for the rent of the property?

Since I have done a simple regression model with my previous project (["GDP_Fertility_Mortality_Relation"](https://github.com/chilam27/GDP_Fertility_Mortality_Relation/edit/master/README.md)), I want to improve my skill sets and prediction's accuracy even more. In this project, I have three main focuses:
1. Learn how to scrape website with Python.
2. Understand the importance of Exploratory Data Analysis and how it contributes to the outcome.
3. Introduce productionization stage into my project.

One more improvement I apply for this project is using different regression models and improve its performance by fine tunning the parameters using `GridSearchCV`.

## Prerequisites

Python Version: 3.7.4

Packages: BeautifulSoup, json, urllib, pandas, numpy, sklearn, matplotlib, seaborn, scipy, statsmodels, xgboost, pickle, flask.

Web Framework Requirements: `pip install -r requirements.txt`

## Project Outline

1. Data collection: use `BeautifulSoup` to scrape property data from Trulia, a popular real estate website. Gather all listed variables that can be used for data analysis.

2. Data cleaning: read in data and prepare it for data analysis. Steps include: tidy up the categorical features, deal with null value, etc.

3. Exploratory data analysis (EDA): examine the cleaned data and its trends so we can choose an approriate model that can be applied.

4. Model building: determine which model (`Linear`, `Lasso`, `Random Forest`, `XGBoost`) work best (that return the smallest error) and tune the model with different parameters using `GridSearchCV`.

5. Productioniize model: create a _local_ API to get quick access to the regression model with a given input set.

To evalutae the performance of our model, I will use the mean absolute error (MAE) as the metric for this project. The reason for choosing this metric is because it can represent clearly, on average, how far off our prediction is. 

### [Data Collection](https://github.com/chilam27/Boston_Housing_Prices/blob/master/P02_DataCollection.py)

I want to give the acknowledgement of this scrapping code to Karishma Parashar (the github repository for her code can be found [here](https://github.com/Abmun/WebScraping-RentalProperties)). Her code gives a really nice outline for the process. Though there are some bugs that I needed to fix in order for the code to run properly and to get the data and the amount I needed.

I started the scrapping procedure on June 25h, 2020. My goal is to scrape, at most, 240 records (not all search term will result with at least 240 records) from each neighborhood of Boston and convert it to a csv file. I have collected 3,894 records and 12 different variables (["housing_data_scraped.csv"](https://github.com/chilam27/Boston_Housing_Prices/blob/master/housing_data_scraped.csv)).

```
Neighborhoods as search key terms: East Boston, Charlestown, Allston, North End, West End, Downtown, Chinatown, Back Bay/ Beacon Hill, South Boston, South End, Fenway, Mission Hill, Roxbury, Dorchester, Jamaica Plain, Mattapan, Roslindale, West Roxbury, Hyde Park.
```
  
Variables             |  Description
:--------------------:|:----------------------------------------------------:
rent                  | the rent of the property for 1 month
address               |  the address of the property
area                  | neighborhood the property located
bed                   | number of beds provided
bath                  | number of bathrooms provided
school                | number of school around the area
crime                 | crime rate of the area
commute               | percentage of people commute by car
shop_eat              | number of shops and restaurants in the area
descroption           | description of the property
feature               | item that property provides (heating, laundry, etc.)
URL                   | link to the property

### Data Cleaning

* Check for null value and remove duplicate.

* Clean up the text for each column.

* 'area' column: rename North End, Downtown, Chinatown and West End to Central; rename South Dorchester and North Dorchester as Dorchester; rename Beacon Hill and Back Bay as Back Bay/ Beacon Hill.

* 'school' column: split values in column accordingly and add value to these new columns: 'elementary_school', 'middle_school', and 'high_school'; delete 'school' column.

* 'shop_eat' column: split values in column accordingly and add value to these new columns: 'restaurant', 'grocery', and 'nightlife'; delete 'shop_eat' column.

* 'feature' column: split values in column accordingly and add value to these new columns: 'property_type', 'pet_allowed', 'laundry', 'parking', 'ac', 'dishwasher', 'washer', 'dryer', 'fridge', and 'total_amenties'; delete 'feature' column.

* Change data type accordingly to the variable and reorder columns

* Deleting unnecessary columns: 'description', 'address', 'url'.

Below is an image of what the dataframe looks like:

<p align="center">
  <img width="1000" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/df.png">
</p>

### Exploratory Data Analysis

* Analyze our target variable - 'rent': caculate the skewness and kurtosis of the variable; plot the value and examine if the distribution shape is normal. Since the original data has high positve skewness and kurtosis (the curve is formed by a huge cluster of mid-range properties and few expensive properties that cause it to have a right skew), I normalize the data by performing log transformation and it resulted very close to a normal distribution.

<p align="center">
  <img width="900" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig1.png">
</p>

<p align="center">
  <img width="800" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig2.png">
</p>

* Then I explore the 'area' variable because I assume that: depends on the neighborhood, the general trend for the rent of a property might be different. Here, I make a pie chart shows the porportion of area that each neighborhood take up and a boxplot of relationship between 'area' and 'rent'. By looking at the mean and its interquatile range, there seems to be some correlation. Another thing to worth noting is the amount of outliers presented in almost every neighborhood.

<p align="center">
  <img width="460" height="400" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig3.png">
</p>

<p align="center">
  <img width="1000" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig4.png">
</p>

* Determine the numerical and categorical variables:

```
Numerical: 'rent', 'bed', 'bath', 'school', 'elemenatary_school', 'middle_school', 'high_school', 'car_commute_percent', 'total_amenties', 'laundry', 'ac', 'dishwasher', 'washer', 'dryer', 'fridge', 'pet_allowed', 'parking', 'restaurant', 'grocery', 'nightlife'.
Categorical: 'area', 'property_type', 'crime'.
```

### Regression Model



### Overall Model Performance



### Productionization



## Conclusion



## Author

* **Chi Lam**, _student_ at Michigan State University - [chilam27](https://github.com/chilam27)

## Acknowledgments

[Amipara, Kevin. Better Visualization of Pie Charts by MatPlotLib. 20 Nov. 2019.](medium.com/@kvnamipara/a-better-visualisation-of-pie-charts-by-matplotlib-935b7667d77f)

[Crossman, Ashley. Understanding Stratified Samples and How to Make Them. 27 Jan. 2020.](www.thoughtco.com/stratified-sampling-3026731)

[I., Chris. Productionize a Machine Learning Model with Flask and Heroku. 9 Dec. 2019](towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2)

[Irekponor, Victor E. CREATING AN UNBIASED TEST-SET FOR YOUR MODEL USING STRATIFIED SAMPLING TECHNIQUE. 14 Nov. 2019](blog.usejournal.com/creating-an-unbiased-test-set-for-your-model-using-stratified-sampling-technique-672b778022d5)

[Marcelino, Pedro. Comprehensive Data Exploration with Python. 23 Aug. 2019.](www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python)

[Science Buddies. Sample Size: How Many Survey Participants Do I Need? 10 Aug. 2017.](www.sciencebuddies.org/science-fair-projects/references/sample-size-surveys)

[Sharma, Natasha. Ways to Detect and Remove the Outliers. 23 May 2018.](towardsdatascience.com/ways-to-detect-and-remove-the-outliers-404d16608dba)
