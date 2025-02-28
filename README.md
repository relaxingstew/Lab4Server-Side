** Notes
API link: https://www.fbi.gov/wanted/api


** Examples

import requests
import json

response = requests.get('https://api.fbi.gov/wanted/v1/list')
data = json.loads(response.content)
print(data['total'])
print(data['items'][0]['title'])

*** Example providing search parameters:

import requests
import json

response = requests.get('https://api.fbi.gov/wanted/v1/list', params={
    'field_offices': 'miami'
})
data = json.loads(response.content)
print(data['total'])
print(data['items'][0]['title'])

*** Example with paging:

import requests
import json

response = requests.get('https://api.fbi.gov/wanted/v1/list', params={
    'page': 2
})
data = json.loads(response.content)
print(data['page'])
print(data['items'][0]['title'])
