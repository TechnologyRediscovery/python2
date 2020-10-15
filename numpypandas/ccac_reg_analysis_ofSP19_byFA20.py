#!/usr/bin/env python
# coding: utf-8

# In[19]:


# Pandas introduction using a flat file of all registrations for courses at CCAC during
# spring 2019:
# What programs are home to students whose mid-term grades are, on average, lower than 
# other? Are mid-term grades good predictors of final grades?
# How likely is a C or lower at MT to lead to a withdraw or F?

import pandas as pd
import numpy as np
import matplotlib as plt
# Special magic function for enabling pyplot charts in jupyter
get_ipython().run_line_magic('matplotlib', 'inline')

# read in the CSV, it's pretty to start with, so that's easy
stud_records = pd.read_csv('19sp_gradestud_only_clean.csv')
stud_records.dtypes
# get just the department column (indexes always come with a Series) in a DF
stud_records.dtypes
stud_records


# In[25]:


# Get unique value counts
stud_records['Department'].value_counts()

degs = stud_records['DegreeType'].value_counts()
print(degs)
# verify that I got a series object out of our data frame when I select only one Column
type(degs)
l = degs.to_list()
# standard python built-in objects
for val in l:
    print(val)


# In[31]:


stud_records


# In[38]:


# Slice the dataframe to only show rows with ID 56400 through 56408
stud_records.iloc[56400:56408]
recs = stud_records

# Make me a data frame of all records of student registrations in online sections
# our lambda function will be applied to each value in "LocationType column"
# and ask "Is Your Value in this list?". The resulting t/f value is used to 
# by the loc function to choose which rows to "locate" and include in our resulting frame
cyber = recs.loc[lambda recs: recs['LocationType'].isin(['Online',])]
print("Cyber: ", len(cyber))
onsite = recs.loc[lambda recs: recs['LocationType'].isin(['On-site',])]
print("OnSite ", len(onsite))


# In[48]:


# Visualize the shape of the cred_start variable for each of our sub-groups
plt.pyplot.hist(cyber['creditStart'])


# In[49]:


plt.pyplot.hist(onsite['creditStart'])

