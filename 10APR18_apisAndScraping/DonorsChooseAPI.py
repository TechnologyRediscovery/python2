
# coding: utf-8

# In[1]:


# iterates over a text file with one keyword per line
# for each keyword, call the API server and capture the JSON response
def readKeyWordFile():
    for keyWord in open('keywords.txt', newline='\n'):
        apiURL = 'https://api.donorschoose.org/common/json_feed.html?keywords="%s"&APIKey=DONORSCHOOSE&showSynopsis=true&max=50' % (keyWord.rstrip())
        # Pass entire json blob from server to method to give us back an average value
        result = getAverageRequestByKeyWord(apiURL)
        print(keyWord.strip() + ": $" + str(result))


# In[2]:


import requests, json
def getAverageRequestByKeyWord(url):
    req = requests.get(url)
    runningTotal = 0
    numProps = 0
    avg = 0
    # check status code for 200 (all ok)
    if(int(req.status_code)==200):
        # get the text of the request with req.text
        # send this into json.loads to create a native object setup
        apiDict = json.loads(req.text)
#         Uncomment this to see the actual dictionary we made from the JSON
#         print(apiDict)
        # navigate the dictionary with standard dict synytax
        proposalList = apiDict['proposals']
        # process the data in the dictionary using a for loop
        for p in proposalList:
            runningTotal = runningTotal + float(p['totalPrice'])
        avg = runningTotal / len(proposalList)
        return avg


# In[3]:


readKeyWordFile()


# In[4]:


import pandas

