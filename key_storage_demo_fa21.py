
# coding: utf-8

# In[11]:


# Demo of accessing an API key--restricted data--
# stored in a file outside this git repo
import json

def retrieve_api_key(key_file_path, key_name):
    '''
        Access a JSON file outside this repo
        and return the value mapped to the inputted key_name
    '''
    k = ""
    try:
        with open(key_file_path, 'r') as keyfile:
            keydict = json.load(keyfile)
            k = keydict[key_name]
    except FileNotFoundError:
        print("Cound not find key file: ", key_file_path)
    except KeyError:
        print("Keyfile does not contain keyname ", key_name)
    return k


# In[13]:


retrievedkey = retrieve_api_key('/home/cogconnect2/.gardening/ecdkeys.json'                                ,'brickset')

