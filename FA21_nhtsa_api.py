
# coding: utf-8

# In[ ]:


# NHTSA API Demo
# Question: Do US Car Makers on average issue more recalls 
# than foreign-built models?
#Narrower: Does Ford issue more recalls on average 
# per model than Audi per model?

# PHASE 1: Assemble a list of all models and model years
# for each of my two manufacturers: Ford, Audi
# sample data structure
# fordmodels=['ranger', 'focus', 'f-150']
# modelyears={'ranger':[1990,1991,1992]}

# PHASE 2: Ingest my model and year data to make
# queries against the recall side of the NHTSA database
# to build a data structure of actual recall info
# Build dictionary of recall notices keyed 
# first by make, then modelyear
# {'ford':{'ranger':{'1999':['recall notice 1', 'recall notice 2']
#                    '2000':['recall notice 1', 'recall notice 2']}   }
#  'audi':{'a42015' :... see above}
# }
#
#Phase 3: Ingest recall data by model and year:
# start with simple counts by model and year
# infer severity somehow? Maybe there's a severity class
# included in data? DO i have to parse the actual recall info
# to infer severity myself?


# In[1]:


import requests

def call_nhtsa(endpoint_ext):
    '''
    Home of my requests to the remote NHTSA server
    Callers must give me everything after the 
    root of NHTSA's api: https://api.nhtsa.gov/
    And will return the RAW text from the response.
    Caller must parse the JSON themselves
    '''
    root='https://api.nhtsa.gov/'
    url = root + endpoint_ext
    response = requests.get(url)
    if(int(response.status_code)==200):
        return response.text
    else:
        raise Exception("Non 200 status code")
    
    


# In[16]:


import json
def lookup_available_years():
    '''
    calls the NHTSA endpoint for getting all possible lookup years
    Plan: Single call here, use output to make multiple calls
    to get_models_by_year_and_make
    '''
    GET_ALL_YEARS = "products/vehicle/modelYears?issueType=r"
    try:
        raw=call_nhtsa(GET_ALL_YEARS)
        obj_res=json.loads(raw)
#         print(obj_res)
        # neato frido list comprehension from a list of
        # of dictionaries whose key is all 'modelyear'
        yearlist = [d['modelYear'] for d in obj_res['results']]
        # NHTSA's year list ends with a nonsense year 9999
        # which is included in the record return count
        # so I'm slicing the final list to exclude the last value
        return yearlist[0:int(obj_res['count'])-1]
    except Exception as ex:
        print(ex)
    
    


# In[19]:


def get_models_by_year_and_make(yr, mk):
    '''
    Takes in a year and a make and returns models
    Plan to make one call to this function for year year and make
    to get models
    sample endpoint 
    products/vehicle/models?modelYear=2010&make=acura&issueType=r
    '''
    url='products/vehicle/models?modelYear=%s&make=%s&issueType=r'%(yr,mk)
    rawresponse=call_nhtsa(url)
    obj=json.loads(rawresponse)
    # parse the JSON response to build just a list of models
    # for further API requesting
    return obj
    


# In[ ]:


def get_recalls_by_make_model_year(mk, mod, yr):
    '''
    Given make, model, and year, returns a list of 
    actual recall notices
    '''
    
    


# In[23]:


all_years = lookup_available_years()
# choose two makes aribitrarily
makes = ['ford', 'Audi']
# test with random year and only one model
models = get_models_by_year_and_make(all_years[60],makes[0])
# iterate over all available years for each make in our study
modellist = []
for mk in makes:
    for yr in all_years:
        res = get_models_by_year_and_make(yr,mk)
        print(mk, ':', yr, '; Acquired ', res['count'], ' records; appending')
        modellist.append(res)
print(modellist)

