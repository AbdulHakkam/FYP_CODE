import requests
import json

startIndex=0
url = "https://services.nvd.nist.gov/rest/json/cves/2.0?startIndex="
nvdData = {}

for i in range(1,2):
    response = requests.get(url+str(startIndex))
    startIndex+=2000
    if i == 1 :
        nvdData = response.json()
    else:
        nvdData['vulnerabilities'].extend(response.json()['vulnerabilities'])
    print(len(nvdData['vulnerabilities'])) 

with open('reports/nvdData.json', 'w') as json_file:
    json.dump(nvdData,json_file, indent=2)