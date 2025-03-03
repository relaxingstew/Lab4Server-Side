import requests
from pydantic import ValidationError
import json
from PIL import Image
from io import BytesIO
from Models import Suspect
import random

fbi_url = "https://api.fbi.gov/wanted/v1/list"
num = random.randint(2,48)
suspects = []

response = requests.get(fbi_url, params={
    'page': num,
    'subjects': 'Most Wanted Terrorists'
    })

if response.status_code == 200 and response != None:
    data = json.loads(response.content)
else:
    response = requests.get(fbi_url, params={
    'page': num,
    'subjects': 'Most Wanted Terrorists'
    })

excluded_subjects = {"Kidnappings/Missing Persons", "Seeking Information", "Crimes Against Children"}

for item in data['items']:
    if 'caution' in item and item['caution'] and 'subjects' in item:
        if not any(sub in excluded_subjects for sub in item['subjects']):
            try:
                suspect = Suspect(
                    name=item.get("title", "Unknown"),
                    crime=item.get("caution", "No description available"),
                    sex = item.get("sex") if item.get("sex") is not None else "Unknown",
                    age=item.get("age_max") or item.get("age_min") or -1, 
                    reward=item.get("reward_max", 0),
                    aliases=", ".join(item.get("aliases", []) or []),  
                    fieldOffice=", ".join(item.get("field_offices", []) or []))
                suspects.append(suspect)
                
            except ValidationError as err:
                print(err)

for suspect in suspects:
    print(suspect)
    print("\n\n\n")
