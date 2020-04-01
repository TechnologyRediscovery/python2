import requests, json
req = requests.get('http://www.nhtsa.gov/webapi/api/Recalls/vehicle/modelyear/2000/make/saturn/model/ls?format=json')
if(int(req.status_code) == 200):
#     print(req.headers.keys())
    apiDict = json.loads(req.text)
    print(apiDict)