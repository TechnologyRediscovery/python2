#!/usr/bin/env python
# coding: utf-8

# In[18]:


from csv import DictReader

# Parsing the Toxic Release Inventory from WPRDC
# https://data.wprdc.org/dataset/toxic-release-inventory/resource/c9baaa77-2dc5-494c-a2ce-f90db9106df2
# We'll use a DictReader object to iterate over the contents of the file and tabulate 
# by year, zip code, carcinogenic status, and company name

# Create data tracking container prior to iterating over our CSV
# empty dicts as values for keys will be added to as we iterate
trisummary = {'incident_count':0,'location':{}, 'year':{},'company':{}}

# use the with facility to manage our file object called trifile
with open('tri_water.csv') as trifile:
    # pass our file object to the DictReader constructor, creating an interable Reader object
    dreader = DictReader(trifile)
    # loop over each row, showing contents
#     print(dreader.fieldnames)
    for record in dreader:
        # tabulate our records as we go
        trisummary['incident_count'] = trisummary['incident_count'] + 1
#         print('Running record count: ', trisummary['incident_count'])
        # check location dict for presence of our current records' zip code
        if record['ZIP_CODE'] not in trisummary['location']:
#             print('Located new ZIP: ', record['ZIP_CODE'])
            # we need to add the zip to our dict, with count 1
            trisummary['location'][record['ZIP_CODE']] = 1
        else:
            # when triggered, our zip code is already in our location dict
            trisummary['location'][record['ZIP_CODE']]+= 1
        if record['REPORTING_YEAR'] not in trisummary['year']:
            print('Located new year: ', record['REPORTING_YEAR'])
            trisummary['year'][record['REPORTING_YEAR']] = 1
        else:
            trisummary['year'][record['REPORTING_YEAR']] += 1
            
print('Summary of records: ', trisummary )
#         print(record['REPORTING_YEAR'])
#         print(record['CARCINOGEN'])
#         print(record['STANDARDIZED_PARENT_COMPANY'])
        # remove routing codes from zip by slicing only the first 5 characters
#         print(record['ZIP_CODE'][0:5])


# In[27]:


prevkey = 0
for y in sorted(trisummary['year']):
    print(y,':',trisummary['year'][y], end='')
    # percent change prev-current / previous
    if prevkey != 0:
        percentdelta = (trisummary['year'][y] - trisummary['year'][prevkey]) /trisummary['year'][prevkey]  
        print(', change: ', percentdelta)
    else:
        print()
    # move our cursor to remember the last key
    prevkey = y

