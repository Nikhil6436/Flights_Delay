# -*- coding: utf-8 -*-
"""Flights_Delay.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jk833wDRoGWWQF-GHhOYBgurgZb61R4K

#Flight Delay prediction
Exploratory Data Analysis

Nikhil Kumar

Mounting the drive to work on the dataset directly from the drive.
"""

from google.colab import drive
drive.mount('/content/gdrive')

import os
os.environ['KAGGLE_CONFIG_DIR'] = "/content/gdrive/My Drive/Kaggle"

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/gdrive/My Drive/Kaggle

!kaggle datasets download -d usdot/flight-delays

!ls

!unzip \*.zip  && rm *.zip

"""Importing relevant **libraries**"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
import pickle

"""Importing the flights dataset"""

flights=pd.read_csv("/content/gdrive/MyDrive/Kaggle/flights.csv")

flights.info()
flights.head()

flights.shape

"""There are 5819079 rows and 31 columns in the dataset.

Getting some basic information from the dataset
"""

number_of_delayed = flights["DEPARTURE_DELAY"].apply(lambda s: 1 if s!=0 else 0);
print("Total number of flights: "+str(len(flights)))
print("Number of cancelled flights: "+str(sum(flights["CANCELLED"])))
print("Number of delayed flights: "+str(sum(number_of_delayed)))
print("Number of diverted flights: "+str(sum(flights["DIVERTED"])))


print("Number of not cancelled flights: "+str(len(flights)-sum(flights["CANCELLED"])))
print("Number of not delayed flights: "+str(len(flights)-sum(number_of_delayed)))
print("Percentage of cancelled flights: "+str((sum(flights["CANCELLED"])*1.0/len(flights))*100)+"%")
print("Percentage of delayed flights: "+str((sum(number_of_delayed)*1.0/len(flights))*100)+"%")

"""Printing no of null values in respective columns"""

flights.isnull().sum()

# fuction to find missing value percetnage
def findmissingval():
    df_missing=pd.DataFrame((flights.isnull().sum()  / flights.shape[0] *100).round(3),columns=['Percentage'])
    return df_missing

# find out the percentage of missing value in each column
df_missing=findmissingval()
df_missing.sort_values(by='Percentage',ascending=False)

"""Dropping unnecessary columns from the dataset which have very large number of null values."""

flights.drop(columns=['AIR_SYSTEM_DELAY','SECURITY_DELAY','AIRLINE_DELAY','LATE_AIRCRAFT_DELAY','WEATHER_DELAY','CANCELLATION_REASON'],inplace=True)

"""Updated dataset"""

flights.head()

"""Finding mode which can be used as 'most likely' in categorical dataset"""

flights.mode()

"""Filling NAN values with appropriate methods , i.e. most likely in place of categorical data , mean for unsigned numerical data which are without reference whereas in case of scheduled time using the corresponding actual time in terms of arrival or departure."""

flights['TAIL_NUMBER'].fillna('N480HA',inplace=True)

flights['DEPARTURE_TIME'].fillna(flights['SCHEDULED_DEPARTURE'],inplace=True)

flights['DEPARTURE_DELAY'].fillna(flights['DEPARTURE_DELAY'].mean(),inplace=True)
flights['TAXI_OUT'].fillna(flights['TAXI_OUT'].mean(),inplace=True)
flights['WHEELS_OFF'].fillna(flights['WHEELS_OFF'].mean(),inplace=True)
flights['SCHEDULED_TIME'].fillna(flights['SCHEDULED_DEPARTURE'],inplace=True)
flights['ELAPSED_TIME'].fillna(flights['ELAPSED_TIME'].mean(),inplace=True)
flights['AIR_TIME'].fillna(flights['AIR_TIME'].mean(),inplace=True)
flights['WHEELS_ON'].fillna(flights['WHEELS_ON'].mean(),inplace=True)
flights['TAXI_IN'].fillna(flights['TAXI_IN'].mean(),inplace=True)
flights['ARRIVAL_TIME'].fillna(flights['SCHEDULED_ARRIVAL'],inplace=True)
flights['ARRIVAL_DELAY'].fillna(flights['ARRIVAL_DELAY'].mean(),inplace=True)

"""All the null values are filled and hence there are no null values."""

flights.isnull().sum()

"""changing the data type of date from object to Date"""

flights['DATE'] = ''
flights['DATE'] = pd.to_datetime(flights[['YEAR', 'MONTH', 'DAY']])

flights.DATE

flights

"""Correlation matrix"""

corr_matrix=flights.corr()
print(corr_matrix)

"""Plotting the Heatmap"""

sns.heatmap(corr_matrix)

"""Dropping the columns that are not relevant for prediction"""

flights = flights.drop(["AIRLINE","FLIGHT_NUMBER","TAIL_NUMBER","DEPARTURE_TIME","DEPARTURE_DELAY","TAXI_OUT", 
                            "WHEELS_OFF","SCHEDULED_TIME","ELAPSED_TIME","AIR_TIME","DISTANCE","WHEELS_ON","TAXI_IN", 
                            "SCHEDULED_ARRIVAL","ARRIVAL_TIME","DIVERTED","AIR_TIME","CANCELLED"], axis = 1)

flights.info()

flights.head()



"""Plotting the Box plot to check the outliers."""

flights[["SCHEDULED_DEPARTURE","ARRIVAL_DELAY"]].plot.box()

"""Removing the outliers from the dataset and reshaping the data"""

Q1 = np.percentile(flights['ARRIVAL_DELAY'], 25, 
                   interpolation = 'midpoint') 
  
Q3 = np.percentile(flights['ARRIVAL_DELAY'], 75,
                   interpolation = 'midpoint') 
IQR = Q3 - Q1 
  
print("Old Shape: ", flights.shape) 
  
# Upper bound
upper = np.where(flights['ARRIVAL_DELAY'] >= (Q3+1.5*IQR))
# Lower bound
lower = np.where(flights['ARRIVAL_DELAY'] <= (Q1-1.5*IQR))
  
#Removing the Outliers
flights.drop(upper[0], inplace = True)
flights.drop(lower[0], inplace = True)
  
print("New Shape: ", flights.shape)

"""Again checking the outliers using the Box Plot"""

flights[["SCHEDULED_DEPARTURE","ARRIVAL_DELAY"]].plot.box()

"""Outliers are almost removed.

Plot percentage delay by month
"""

month_count= flights["MONTH"].value_counts()
month_count = month_count.sort_index()
month = np.array(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
y_pos=np.arange(len(month))

fig=plt.figure()
ax=fig.add_subplot(111)
ax.bar(month,month_count,align='center',alpha=0.5,color='cyan')
ax.set_facecolor('gray')
plt.xticks(y_pos,month)
plt.ylabel('Flight Counts')
plt.title('Flight Counts by Month')
plt.show()

"""Plot percentage delay by Day"""

day_count= flights["DAY_OF_WEEK"].value_counts()
day_count = day_count.sort_index()
day= np.array(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
y_pos=np.arange(len(day))

fig=plt.figure()
ax=fig.add_subplot(111)
ax.bar(day,day_count,align='center',alpha=0.5,color='cyan')
ax.set_facecolor('gray')
plt.xticks(y_pos, day,rotation=90)
plt.ylabel('Flight Counts')
plt.title('Flight Counts by Day')
plt.show()

"""Which months had the highest percentage of departure and arrival delays?

Plotting Histogram for numerical data to chek the distribution of the data in different columns.
"""

sns.distplot( flights['ARRIVAL_DELAY'])

sns.distplot( flights['SCHEDULED_DEPARTURE'])

"""Here we find that most of the columns are normally distributed.

Plotting the bar graph for categorical data to check the distribution.

New feature generation as RESULT using ARRIVAL_DELAY
"""

#FEATURE GENERATION FROM ARRIVAL_DELAY, USING IF ELSE STATEMENT:
flights['RESULT']=flights['ARRIVAL_DELAY'].apply(lambda x: 1 if x>15 else 0)
flights.head()

flights.RESULT.value_counts()

flights.SCHEDULED_DEPARTURE.value_counts()

"""**EXploratory Data Analysis ,Data Cleaning and Pre-processing for Flights dataset is complete.**

**Exploratory Data Analysis of Weather2 dataset.**
"""

weather2=pd.read_csv("weather2.csv")
weather2.info()
weather2.head()

weather2.shape

# fuction to find missing value percetnage
def findmissingval():
    df_missing=pd.DataFrame((weather2.isnull().sum()  / weather2.shape[0] *100).round(3),columns=['Percentage'])
    return df_missing

# find out the percentage of missing value in each column
df_missing=findmissingval()
df_missing.sort_values(by='Percentage',ascending=False)

# select columns having more than 40% missing values.
columnstodrop=df_missing[df_missing['Percentage'] > 40]
columnstodrop.index

# drop the columns which having more than 40% missing values
weather2=weather2.drop(columnstodrop.index,axis=1)

# find out the percentage of missing value in each column
df_missing=findmissingval()
df_missing.sort_values(by='Percentage',ascending=False)

weather2.info()

weather2.isnull().sum()

"""Filling the NA values with mean"""

weather2['WSF5'].fillna(weather2['WSF5'].mean(),inplace=True)
weather2['WDF5'].fillna(weather2['WDF5'].mean(),inplace=True)

weather2.isnull().sum()

weather2

weather2.DATE

"""Changing data type of Date"""

weather2.DATE=pd.to_datetime(weather2.DATE)

weather2.DATE

"""Correlation matrix"""

weather2.corr()

"""Heatmap"""

sns.heatmap(weather2.corr())

"""Plotting Scatter matrix to see the relationships between two variables."""

pd.plotting.scatter_matrix(weather2)

"""Box plot """

weather2[['AWND', 'PRCP', 'TAVG', 'TMAX', 'TMIN']].plot.box()

f, axes = plt.subplots(3, 3, figsize=(25,25))
sns.distplot( weather2['WSF5'],ax=axes[0, 0])
sns.distplot( weather2['AWND'], ax=axes[0, 1])
sns.distplot( weather2['TMAX'], ax=axes[0, 2])
sns.distplot( weather2['TMIN'], ax=axes[1, 0])
sns.distplot( weather2['TAVG'], ax=axes[1, 1])
sns.distplot( weather2['PRCP'], ax=axes[1, 2])
sns.distplot( weather2['WDF2'], ax=axes[2, 0])
sns.distplot( weather2['WDF5'], ax=axes[2, 1])
sns.distplot( weather2['WSF2'], ax=axes[2, 2])



"""**Exploratory Data Analysis ,Data Cleaning and Pre-processing for weather2 dataset is complete.**

Taking random sample from flights dataset
"""

f=flights.sample(1000)

"""Merging the two dataset using DATE feature"""

f1=pd.merge(f,weather2,on='DATE',how='inner')

f1

f1.info()

"""Dropping irrelevant features for better prediction"""

f1.drop(['YEAR','MONTH','DAY','DATE','ORIGIN_AIRPORT','DESTINATION_AIRPORT','STATION','NAME','DAY_OF_WEEK'],axis=1,inplace=True)

f1.isnull().sum()

"""Importing relevant libraries for model building"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.preprocessing import MinMaxScaler
import math

"""selecting the independent variables"""

x=f1.drop('RESULT',axis=1)

x.shape

"""Selecting the dependent variable"""

y=f1.RESULT

"""Scaling the dataset"""

scaler=MinMaxScaler(feature_range=(0,1))
x=scaler.fit_transform(x)

sns.displot(y)

x

"""Splitting into training and test dataset"""

X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.3,random_state=100)

"""Here model1 , model2 and model3 represents Logistic Regression , Decision Tree and Random Forest models respectively."""

model1=LogisticRegression()
model2=DecisionTreeRegressor()
model3=RandomForestRegressor()

"""Training the models"""

model1.fit(X_train,Y_train)

model2.fit(X_train,Y_train)

model3.fit(X_train,Y_train)

"""Predicting the values"""

pred1=model1.predict(X_test)

pred2=model2.predict(X_test)

pred3=model3.predict(X_test)

"""Importing relevant libraries for model accuracy"""

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score,recall_score,f1_score,roc_auc_score,roc_curve,accuracy_score

"""Confusion matrix for logistic regression"""

print("Confusion matrix for logistic regression:")
confusion_matrix(Y_test,pred1)

"""Accuracy check for logistic regression"""

accuracy=0
for i in range(len(pred1)):
  if pred1[i]==Y_test.iloc[i]:
    accuracy +=1
Accuracy = accuracy/(len(pred1))
print("Accuracy for logistic regression model:",Accuracy) 
print("Accuracy_score for logistic regression model",accuracy_score(Y_test,pred1))
print("roc auc score for logistic regression model",roc_auc_score(Y_test,pred1))
print('precision score for logistic regression model is:',precision_score(Y_test,pred1))
print("recall score for logistic regression model:",recall_score(Y_test,pred1))
print("f1 score for logistic regression model:",f1_score(Y_test,pred1))

"""Confusion Matrix for Decision Tree model"""

print("Confusion matrix for Decision Tree Model:")
confusion_matrix(Y_test,pred1)

"""Accuracy check for Decision Tree model"""

accuracy2=0
for i in range(len(pred2)):
  if pred2[i]==Y_test.iloc[i]:
    accuracy2 +=1
Accuracy2 = accuracy2/(len(pred2))
print("Accuracy for Decision tree model:",Accuracy2) 
print("Accuracy_score for Decision tree model",accuracy_score(Y_test,pred2))
print("roc auc score for Decision tree model",roc_auc_score(Y_test,pred2))
print('precision score for Decision tree model:',precision_score(Y_test,pred2))
print("recall score for Decision tree model:",recall_score(Y_test,pred2))
print("f1 score for Decision tree model:",f1_score(Y_test,pred2))

"""Accuracy of Random Forest model"""

accuracy3=0
for i in range(len(pred3)):
  if pred3[i]==Y_test.iloc[i]:
    accuracy3 +=1
Accuracy3 = accuracy3/(len(pred3)) 
print("Accuracy for Random Forest model:",Accuracy3)

pickle.dump(model1, open('model.pkl',"wb"))



""" **Thank you**"""

