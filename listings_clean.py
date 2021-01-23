# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:12:50 2021

@author: Liz
"""

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
os.chdir("C:\\Users\\labbi\\OneDrive\\Liz\\projects\\Airbnb\\data")

#Dataset: listings_details
listings_details = pd.read_csv("listings_details.csv")
listings_details.columns
len(listings_details)

#number of listing
num = len(pd.unique(listings_details['id']))
print(num)
#check scrape details
listings_details['calendar_last_scraped'].value_counts()
num_listings = pd.DataFrame(listings_details['calendar_last_scraped'].value_counts()[:9,])
num_listings['month'] = pd.DatetimeIndex(num_listings.index).month
num_listings = num_listings.sort_values('month', ascending=True)

#plot
fig,ax = plt.subplots(1,1)
x = num_listings['month']
y = num_listings['calendar_last_scraped']
ax.plot(x, y, color = '#FF5A5F')
ax.set_title("Number of listings by months")
ax.set_xlabel('Months')
ax.set_ylabel('Number of listings')
ax.set_ylim([3000,6500])
plt.savefig('numoflistings.jpg',dpi=150)
plt.show()

#keep only the lastest scraped data of listings
listings_details['calendar_last_scraped'] = pd.to_datetime(listings_details['calendar_last_scraped'])
listings_details = listings_details.sort_values(by=['calendar_last_scraped']).drop_duplicates(subset='id', keep='last')
#check
assert len(listings_details) == num
'''
#plot 
num_listings1 = listings_details['host_since'].value_counts()
num_listings1 = num_listings1.reset_index()
num_listings1['date'] = pd.to_datetime(num_listings1['index'])
num_listings1 = num_listings1.sort_values('date', ascending=True)
num_listings1['cumsum'] = num_listings1['host_since'].cumsum()

num_listings2 = listings_details['last_review'].value_counts()
num_listings2 = num_listings2.reset_index()
num_listings2['date'] = pd.to_datetime(num_listings2['index'])
num_listings2 = num_listings2.sort_values('date', ascending=True)

num_listings1['cumsum'] = num_listings1['host_since'].cumsum()
'''
#check nan
listings_details.isnull().values.any()
listings_details.isnull().sum().sum()
listings_details.isnull().sum()

nan_tb = listings_details.isnull().sum()
nan_vars = list(nan_tb[nan_tb>8000].index)
listings_details = listings_details.drop(nan_vars, axis = 1)

#drop variables
#drop vars that have less deversity
col_unique = listings_details.nunique(axis=0)
print(col_unique[col_unique == 1])
drop_colnames = list(col_unique[col_unique == 1].index)
listings_details = listings_details.drop(drop_colnames, axis = 1)

#drop url
url_colnames = listings_details.columns[listings_details.columns.str.contains(pat = 'url')] 
listings_details = listings_details.drop(url_colnames, axis = 1)

#drop scrape
scrape_colnames = listings_details.columns[listings_details.columns.str.contains(pat = 'scrape')] 
listings_details = listings_details.drop(scrape_colnames, axis = 1)

#drop host
host_columns = listings_details.columns[listings_details.columns.str.contains(pat = 'host')]
keep_vars = {'host_since','host_response_time','host_response_rate',
             'host_is_superhost','host_has_profile_pic', 'host_identity_verified'}
host_columns = [ele for ele in host_columns if ele not in keep_vars]
listings_details = listings_details.drop(host_columns, axis = 1)
listings_details = listings_details.drop(['host_response_time'], axis = 1)

#drop address vars
#listings_details['state'].value_counts()
address_vars = ['market','state','jurisdiction_names','street','city','neighbourhood','smart_location','zipcode','latitude','longitude']
listings_details = listings_details.drop(address_vars, axis = 1)

#drop text
text_vars = ['name','summary','space','description','neighborhood_overview','notes','transit',
             'access','interaction','house_rules','amenities']
listings_details = listings_details.drop(text_vars, axis = 1)

#drop reviews
review_vars = ['number_of_reviews_ltm','first_review', 'last_review']
listings_details = listings_details.drop(review_vars, axis = 1)
#drop other vars
other_vars = ['instant_bookable','require_guest_profile_picture',
              'require_guest_phone_verification','calendar_updated']
listings_details = listings_details.drop(other_vars, axis = 1)

#drop price
listings_details = listings_details.drop(['price'], axis = 1)

#final number of columns:45
listings_details.columns
listings_details.isnull().sum()

#clean vars
listings_details['host_response_rate'] = listings_details['host_response_rate'].str.replace("%", "").astype(float)
listings_details['security_deposit'] = listings_details['security_deposit'].str.replace("[$,]", "").astype(float)
listings_details['cleaning_fee'] = listings_details['cleaning_fee'].str.replace("[$,]", "").astype(float)
listings_details['extra_people'] = listings_details['extra_people'].str.replace("[$,]", "").astype(float)

#fill na
listings_details = listings_details.fillna(listings_details.mean())
listings_details.isnull().sum()

#deep clean
listings_details['host_since'] = pd.to_datetime(listings_details['host_since'])
listings_details['host_since'] = round((pd.to_datetime('11/01/19') - listings_details['host_since']).dt.days/365,3)

tf_col = listings_details.nunique(axis=0)
tf_vars = list(tf_col[tf_col == 2].index)

for col in tf_vars:
    listings_details[col] = pd.Series(np.where(listings_details[col].values == 't', 1, 0),listings_details.index)

#save file
listings_details.to_csv('listings_details_clean.csv',index=False)

