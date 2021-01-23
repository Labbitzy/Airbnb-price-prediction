# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 13:55:29 2021

@author: Liz
"""

import os
import pandas as pd
from matplotlib import pyplot as plt
os.chdir("C:\\Users\\labbi\\OneDrive\\Liz\\projects\\Airbnb\\data")

#Dataset: calendar
calendar = pd.read_csv("calendar.csv")
calendar.head()
#number of listing:8806
print(len(pd.unique(calendar['listing_id'])))
#time length
#first: 2019-01-17 last:2020-10-09 unique:632
calendar['date'] = pd.to_datetime(calendar['date'], format="%Y-%m-%d")
calendar['date'].describe()

#check nan
calendar.isnull().values.any()
calendar.isnull().sum().sum()
calendar.isnull().sum()

#nan columns
nan_values = calendar.isna()
nan_columns = nan_values.any()
columns_with_nan = calendar.columns[nan_columns].tolist()
print(columns_with_nan)

#drop nan
calendar = calendar.dropna()
calendar.isnull().sum().sum()

#clean price
calendar['price'] = calendar['price'].str.replace("[$,]", "").astype(float)
calendar['adjusted_price'] = calendar['adjusted_price'].str.replace("[$,]", "").astype(float)
calendar['price'].describe()
calendar['adjusted_price'].describe()

#compare price and adjust price
sum(calendar['price'] != calendar['adjusted_price'])
calendar[calendar['price'] != calendar['adjusted_price']]['listing_id'].value_counts()
calendar = calendar.drop(['adjusted_price'], axis = 1)

#avgerage price 223.06
avg_price = calendar['price'].mean() 

#mean price of the listings
avg_price = calendar.groupby(['listing_id']).mean()

#remove outliers
avg_price = avg_price[avg_price['price']<=1000]
#plot
fig,ax = plt.subplots(1,1)
x = avg_price.iloc[:,0]
ax.hist(x, bins = 50, color = '#FF5A5F')
ax.set_title("Distribution of listing price")
ax.set_xlabel('Price')
ax.set_ylabel('Freq. of price')
plt.savefig('pricedistribution2.jpg',dpi=150)
plt.show()

#price by weekdays
calendar['weekday'] = pd.to_datetime(calendar['date']).dt.day_name()
avg_price = calendar.groupby(['weekday']).mean()
avg_price = avg_price.reindex(['Monday','Tuesday', 'Wednesday','Thursday','Friday','Saturday', 'Sunday'])

#plot
#listing price is higher on Friday and Saturday
fig,ax = plt.subplots(1,1)
x = avg_price.index
y = avg_price['price']
ax.plot(x, y, color = '#FF5A5F')
ax.set_title("Avg. listing price by weekdays")
ax.set_xlabel('Weekdays')
ax.set_ylabel('Price')
plt.savefig('pricedistribution3.jpg',dpi=150)
plt.show()

#price by months
calendar['month'] = pd.DatetimeIndex(calendar['date']).month
avg_price_month = calendar.groupby(['month']).mean()
avg_price_month = avg_price_month.round(2)

#prices in summer season are higher than winter seasons
fig,ax = plt.subplots(1,1)
x = avg_price_month.index
y = avg_price_month['price']
ax.plot(x, y, color = '#FF5A5F')
ax.set_title("Avg. listing price by months")
ax.set_xlabel('Months')
ax.set_ylabel('Price')
plt.savefig('pricedistribution4.jpg',dpi=150)
plt.show()

#clean data
calendar['weekday'] = calendar['weekday'].apply(lambda x: 1 if (x == 'Friday')| (x == 'Saturday')else 0)
calendar['month'] = calendar['month'].apply(lambda x: avg_price_month['price'][x]/avg_price)
calendar = calendar.drop(['available','date'], axis = 1)

calendar.columns
calendar.head()

#save file
calendar.to_csv('calendar_clean.csv',index=False)
