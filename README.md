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

One more improvement I apply in this project is using different regression models and improve its performance by fine tunning the parameters using `GridSearchCV`.

## Prerequisites

Python Version: 3.7.4

Packages: BeautifulSoup, json, urllib, pandas, numpy, sklearn, matplotlib, seaborn, scipy, statsmodels, xgboost, pickle, flask.

Web Framework Requirements: `pip install -r requirements.txt`

## Project Outline

1. Data collection: use `BeautifulSoup` to scrape property data from Trulia, a popular real estate website. Gather all listed variables that can be used for data analysis.

2. Data cleaning: read in data and prepare it for data analysis; steps include: tidy up the categorical features, deal with null value, etc.

3. Exploratory data analysis (EDA): examine the cleaned data and its trends so we can choose an approriate model that can be applied.

4. Model building: determine which model (`Linear`, `Lasso`, `Random Forest`, `XGBoost`) work best (that return the smallest error) and tune the model with different parameters using `GridSearchCV`.

5. Productioniize model: create a _local_ API to get quick access to the regression model with a given input set.

To evalutae the performance of our model, I will use the mean absolute error (MAE) as the metric for this project. The reason for choosing this metric is because it can represent clearly, on average, how far off our prediction is. 

### [Data Collection](https://github.com/chilam27/Boston_Housing_Prices/blob/master/P02_DataCollection.py)

_*Disclaimer: this data set is used for educational puspose._

I want to give the acknowledgement of this scrapping code to Karishma Parashar (the github repository for her code can be found [here](https://github.com/Abmun/WebScraping-RentalProperties)). Her code gives a really nice outline for the process. Though there are some bugs that I needed to fix in order for the code to run properly and to get the data and the amount I needed.

I started the scrapping procedure on June 25h, 2020. My goal is to scrape, at most, 240 records (not all search term will result with at least 240 records) from each neighborhood of Boston and convert it to a csv file. I have collected 3,894 records and 12 different variables (["housing_data_scraped.csv"](https://github.com/chilam27/Boston_Housing_Prices/blob/master/housing_data_scraped.csv)). 

One thing to note is the 'feature' variable: I could not code the scrapping process to attain all features because of the 'See All" button that hide some of the data. Do not rely heavily on this variable when doing analysis.

Neighborhoods as search key terms: East Boston, Charlestown, Allston, North End, West End, Downtown, Chinatown, Back Bay/ Beacon Hill, South Boston, South End, Fenway, Mission Hill, Roxbury, Dorchester, Jamaica Plain, Mattapan, Roslindale, West Roxbury, Hyde Park.
  
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

### [Data Cleaning](https://github.com/chilam27/Boston_Housing_Prices/blob/master/P02_DataCleaning.py)

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
  <img width="1000" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig1.png">
</p>

### [EDA](https://github.com/chilam27/Boston_Housing_Prices/blob/master/P02_EDA.py)

* Here is the general description of our variables: we have no missing value or any null value and all the data types are in place.

  <p align="center">
  <img width="400" height="600" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig2.png">
</p>

* Univariate analysis on target variable ('rent'): caculate the skewness and kurtosis of the variable; plot the value and examine if the distribution shape is normal. From the table and graph, we can see that: since the original data has high positve skewness and kurtosis (the curve is formed by a huge cluster of mid-range properties and few expensive properties that cause it to have a right skew), I normalize the data by performing log transformation and it resulted very close to a normal distribution.

<p align="center">
  <img width="300" height="200" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig3.png">
</p>

<p align="center">
  <img width="900" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig4.png">
</p>

<p align="center">
  <img width="800" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig5.png">
</p>

* Multivariate analysis on target variable: have bathroom as an addition dependent variable and see the relationship between rent and number of bathroom a property has. With the plot below, there is an upward trend.

<img width="400" height="400" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig6.png">  <img width="400" height="400" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig7.png">

* Remove outliers: I use Z-score to help me identify and remove outliers from the dataframe. This has improved the distribution by a great amount.

<p align="center">
  <img width="800" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig8.png">
</p>

* Determine the numerical and categorical variables

  - Numerical: 'rent', 'bed', 'bath', 'school', 'elemenatary_school', 'middle_school', 'high_school', 'car_commute_percent', 'total_amenties', 'laundry', 'ac', 'dishwasher', 'washer', 'dryer', 'fridge', 'pet_allowed', 'parking', 'restaurant', 'grocery', 'nightlife'.
  - Categorical: 'area', 'property_type', 'crime'.

* Observe to see how variables are correlated to each other through heatmap: from this plot, there are many interesting details that we need to pay attention of.

  - 'bed', 'bath', 'restaurant', 'grocery', and 'nightlife', accordingly, have the highest correlation with the target variable. Though they are less correlated than expected.

  - All the schoool variables are highly correlated to each other. This is predicted since the values were derived from a single variable during our cleaning phase. Similar can be said with 'restaurant', 'grocery', and 'nightlife' (they came from a variable that is called 'shop_eat')

  - All the features variables interesting have lower correlation with the target variable. Keep in mind that we will not use much of these data.

<p align="center">
  <img width="900" height="700" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig9.png">
</p>

* Observed only those numerical variables that has high correlation with target variable with zoomed heatmap. Since we have mentions that 'restaurant', 'grocery', and 'nightlife' are pretty similar, we can remove two of the variables and keep 'grocery' for now for analysis (figure 12)

<img width="250" height="600" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig10.png"> <img width="500" height="600" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig11.png">

<p align="center">
  <img width="600" height="500" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig12.png">
</p>

* Next is to examine the cateogircal variable. I explore the 'area' variable with the assumption that: depends on the neighborhood, the general trend for the rent of a property might be different. Here, I make a pie chart shows the porportion of area that each neighborhood take up and a boxplot of relationship between 'area' and 'rent'. By looking at the mean and its ranges, there seems to be some correlation. Another thing to worth noting is the amount of outliers presented in almost every neighborhood.

<img width="400" height="400" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig13.png">  <img width="400" height="400" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig14.png">

<p align="center">
  <img width="1000" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig15.png">
</p>

* Examine 'property_type' and 'crime' and their relation with rent:
  - Because there is an inbalance proportion of data for 'property_type'(appartment 3%, condo >0.1%, multi 96%, single 1%, townhouse and condo are > 1%), it can be hard to examin the relationship accurately.
  - Based on the graph, we can see a representation of what it would look like: multi-family and townhouse has about the same median, a little bit higher than that is single family; although apartment seems to have the same median as a condo, I believe if we have enough data points, condo would be the property with the highest rent.
  - As for 'crime', Moderate and Low crime rates have the same median and range. Although High rate does have a similar median but interestingly has higher range.
  - The two most supring ones are the Lowest and Highest rates: while Lowest one also has the lowest median and, arguably, range, the Highest rate has the highest median. I expected it to be the opposite for these two. Based on this, maybe properties that are more expensive attracts more crime than lower ones?

<p align="center">
  <img width="1000" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig16_17.png">
</p>

* Create dummies variable for the categorical variables: 'area', 'property_type', 'crime'

### [Regression Model](https://github.com/chilam27/Boston_Housing_Prices/blob/master/P02_RegressionModel.py)

* Split the data to training (80%) and testing (20%) sets in a stratify fashion: stratas are the different neighborhood. The reason for this is because I want to have the coverage of the entire area in the Boston city and some neighborhood have significantly lower data than others.

* Testing assumptions - Normality/ Linearity: when I was investigating our rent variable during the EDA stage, I have transformed the data into log so it can prevent underfitting. But I tested it again for our train data to be sure also.

<img width="400" height="400" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig18.png">  <img width="400" height="400" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig19.png">

* Testing assumptions - Homoscedasticity: I included all variables to eliminate heteroscedasticity.
* Testing assumptions - Absence of Multicollinearity: though I have tried to remove variables that are highly correlated to each other, I found in the result of regression models that by including every variable I was able to get a higher accuracy rate.
  
* Ordinary least squares (OLS) regression: by being one of the simplest estimator for simple model, it is easier to implement and interpret compare to other sofiticated ones. Although it might not work well with my project that has many varaibles and correlations to the target is week, I gave it a shot. Beside the table of correlation that I already have a general picture of what it is like, a statistical measurement that I am interested in is the "R-squared" (coefficient of determination) of **0.661**. This means that our model fits well and we can predict about 66.1% of our trained data set. Keep in mind that although the difference between "R-squared" and "Adj. R-squared" (**0.657**)is not too significant, but it let us know that there are some irrelevant features that we have included in our model. Another interesting measurement is "F-statistics" that has value above 100 (*152.3*) and "Prop (F-statistics)" that has value below 0.05 (*0.00*). By having these two measurements meeting the condition, it means that there is a good linear relationship between the taget and all the feature variables. 
```python
X_sm = X = sm.add_constant(X) #create a column of all '1' create an intercept to the slope of the regression line; this is necessary for stats model
del X_sm['area']
model = sm.OLS(np.asarray(y), X_sm.astype(float))
model.fit().summary()
```
<p align="center">
  <img width="800" height="300" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig20.png">
</p>

_Throughout all of the model, I will implement cross validation to eliminate the probability that the model might be over fitting or contains bias_
  
* Multiple linear regression: (this is the same model of what we have discussed above, but I use mean absolute error here as my measurement of the model accuracy)
```python
reg_lin = LinearRegression()
reg_lin.fit(X_train, y_train)
np.mean(cross_val_score(reg_lin, X_train, y_train, scoring = 'neg_mean_absolute_error'))
```
```python
Out[1]: -393.7313
```
  
* Lasso (least absolute shrinkage and selection operator) regression: in contrast with the model above, I tested out Lasso regression model because of its ability to analyze data set with large features very well. That is not the only reason for applying in this model because I want to see how its L1 regularization technique works (helps with eliminating overfitting). For this model, I have tested out a range of alpha from 1 to 100 with an increment of 10. By finding the maximum error of the curve of the plot below, we have alpha = 1.7.

<p align="center">
  <img width="800" height="400" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig21.png">
</p>

```python
reg_las = Lasso(alpha = alpha[y_max_index])
reg_las.fit(X_train, y_train)
np.mean(cross_val_score(reg_las, X_train, y_train, scoring = 'neg_mean_absolute_error'))
```
```python
Out[2]: -392.8202
```

* Random forest regression: this model apply some different techniques to predict the data: it uses multiple decision tree and bagging (or bootstrap aggregation) to better understand the bias and variance of the data. Because it also works well with large data set, I applied this model to our data to see how it does compare to other models.
```python
reg_rf = RandomForestRegressor(random_state = 1)
reg_rf.fit(X_train, y_train)
np.mean(cross_val_score(reg_rf, X_train, y_train, scoring = 'neg_mean_absolute_error'))
```
```python
Out[3]: -306.6928
```

* XGBoost: being known for its ability to outperform any of its competitors, XGBoost is my last algorithm of choice to predict our data. Different from random forest regression, it uses boosting technique (combining weak learners to strong ones to improve prediction accuracy). It is also powerful for the wide range of parameters to really fine tune the algorithm.
```python
reg_xgboost = xgb.XGBRegressor()
reg_xgboost.fit(X_train, y_train)
np.mean(cross_val_score(reg_xgboost, X_train, y_train, scoring = 'neg_mean_absolute_error'))
```
```python
Out[4]: -343.4491
```

### Overall Model Performance

Before finalizing our model, I made three different adjustments to the data to see if it can improve the prediction:
  1. Size: initially, after finished cleanning the data, I trimmed the data set from 3000+ records to about 759 records. I trimmed it based on the proportion of the area that each neighborhood take relative to the area of city. The reason why the size is small is because for neighborhood like Hyde Park and Mattapan has very few records on Trulia. But it turned out that it does not give a very good prediction as if I leave the size as it is. This concluded that the larger the sample size is the better the prediction is.
  2. Stratification: in order for our sample to accuratly represent the city of Boston, I make sure all neighborhood are present in the training data set. As it turned out, this also resulted in a better prediction for our model.
  3. Eliminate irrelavent features: recalling back to our heat maps from above, there are only a few varaibles that give me the correlation with the target variable that is above 0.2. I thought, by removing the irrelevant features and those that highly correlated to each other, would increase the performance. But it did not turn about to be like that. I am still unsure of why this is the case. But by including all variables, it seems to preform better (the larger the number of features is the better?)

There are two things in the list of outcome of our prediction models that suprised me: there is only *0.9* improvement in lasso regression compare to the multiple linear regession and the random forest regression outperformed the XGBoost algorithm by *36.7*. Because of this, I will apply an exhaustive `GridSearchCV` to search for the best parameters for the random forest regression. Although I have tried to exhausted tuning with many more parameters such as "max_depth" and "min_samples_leaf", it took too much time so I did a simple one instead (so the difference of the result is not huge).
```python
parameters = {'n_estimators': [200, 400, 600, 800],
              'criterion': ['mse', 'mae'], 
              'max_features': ['auto','sqrt','log2']}
grid = GridSearchCV(reg_rf, parameters, scoring = 'neg_mean_absolute_error', cv=5)
grid.fit(X_train, y_train)

grid.best_score_
```
```python
Out[5]: -304.3920688932027
```

With the best parameters for our best performance model through the training data set, now it is the time to implement it to our test data set too see how well our model can predict the prices of property in Boston:
```python
reg_lin_test = reg_lin.predict(X_test)  
reg_las_test = reg_las.predict(X_test)
reg_xgboost_test = reg_xgboost.predict(X_test)
reg_rf_test = grid.best_estimator_.predict(X_test)

print('Multiple linear regression: ', mean_absolute_error(y_test, reg_lin_test))
print('Lasso regression: ', mean_absolute_error(y_test, reg_las_test))
print('XGBoost regression: ', mean_absolute_error(y_test, reg_xgboost_test))
print('Random forest regression regression (using best parameters through GridSearchCV): ', mean_absolute_error(y_test, reg_rf_test)) #best one
```
```python
Multiple linear regression:  1469.1753603498644
Lasso regression:  393.3840532780861
XGBoost regression:  403.93248876337
Random forest regression regression (using best parameters through GridSearchCV):  316.51083201892743
```

### [Productionization](https://github.com/chilam27/Boston_Housing_Prices/blob/master/FlaskAPI/app.py)

For this part of the project, I followed Chris I. article "Productionize a Machine Learning model with Flask and Heroku" and applied it for my project.

- Pickle the model to save the model by turning it to byte stream
```python
pickl = {'model': grid.best_estimator_}
pickle.dump(pickl, open( 'model.pkl', "wb")) 
```

- Creating a new python file with a list of ordered input values to act as input for the model.

- Build a Flask (a micro web frame work) API using Flask module by installing the requirements, create new python files and import necessary command for those files (app.py, wsgi.py, requests.py, etc.)

- Apply the input to the model with the working API.

<p align="center">
  <img width="800" height="500" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig22.png">
</p>

## Conclusion

With out best prediction model returns the MAE of 316.51 for the test data set, the model does predict the property's price according to the features that are used quite accurately. The MAE value of 316.51 means that on average, our prediction is off around 316.51. That is acceptable consider how low our correlatation values are. We concluded that a fine tune random forest regression works the best in predicting property's rent based on 19 of the used features.

Although my first intention was to followe the tutorial by Chris I. and productionize the model into a public API with Flask and Heroku, but because I could not spend more time to tackle problems I had with Heroku so I made it local instead (I have attached my progress and the problem that I was on in figures below). 

<p align="center">
  <img width="800" height="500" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig23.png">
</p>

<p align="center">
  <img width="800" height="500" src="https://github.com/chilam27/Boston_Housing_Prices/blob/master/readme_image/fig24.png">
</p>

## Author

* **Chi Lam**, _student_ at Michigan State University - [chilam27](https://github.com/chilam27)

## Acknowledgments

[Amipara, Kevin. Better Visualization of Pie Charts by MatPlotLib. 20 Nov. 2019.](medium.com/@kvnamipara/a-better-visualisation-of-pie-charts-by-matplotlib-935b7667d77f)

[Crossman, Ashley. Understanding Stratified Samples and How to Make Them. 27 Jan. 2020.](www.thoughtco.com/stratified-sampling-3026731)

[E. San San Wong, Cathy Edwards. Public Art Is Alive and Well in Boston Neighborhoods.](www.barrfoundation.org/blog/public-art-in-boston-neighborhoods)

[I., Chris. Productionize a Machine Learning Model with Flask and Heroku. 9 Dec. 2019](towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2)

[Irekponor, Victor E. CREATING AN UNBIASED TEST-SET FOR YOUR MODEL USING STRATIFIED SAMPLING TECHNIQUE. 14 Nov. 2019](blog.usejournal.com/creating-an-unbiased-test-set-for-your-model-using-stratified-sampling-technique-672b778022d5)

[Marcelino, Pedro. Comprehensive Data Exploration with Python. 23 Aug. 2019.](www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python)

[Science Buddies. Sample Size: How Many Survey Participants Do I Need? 10 Aug. 2017.](www.sciencebuddies.org/science-fair-projects/references/sample-size-surveys)

[Sharma, Natasha. Ways to Detect and Remove the Outliers. 23 May 2018.](https://towardsdatascience.com/ways-to-detect-and-remove-the-outliers-404d16608dba)
