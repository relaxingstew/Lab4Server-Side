import requests
from pydantic import ValidationError
import json
from PIL import Image
from io import BytesIO
import Models

fbi_url = "https://api.fbi.gov/wanted/v1/list"
num = input("Enter a number for which page to search on the API: ")

response = requests.get(fbi_url, params={
    'page': num,
    'subjects': 'Most Wanted Terrorists'
})

data = json.loads(response.content)

excluded_subjects = {"Kidnappings/Missing Persons", "Seeking Information", "Crimes Against Children"}

for item in data['items']:
    if 'caution' in item and item['caution'] and 'subjects' in item:
        if not any(sub in excluded_subjects for sub in item['subjects']):
            print(f"{item['title']} - {item['caution'][:100]}...")
