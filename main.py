import requests
from pydantic import ValidationError
import json
from PIL import Image
from io import BytesIO
from Models import Suspect
import random

def game(num, list):
    while True:
        userInp = input(f"Current Points|{num}| Enter [S]uspects [I]nspect [C]rimes [Q]uit or [M]ake a guess:\n")
        userInp = userInp.lower()
        if userInp == "s":
            for suspect in list:
                print(f"Suspect {suspect.susNum} {suspect.name}")    
        if userInp == "c":
            for suspect in list:
                print(f"{suspect.crime}\n")
        elif userInp == "i":
            try:
                suspect_num = int(input("Enter Suspect Number to inspect: "))
                selected_suspect = next((s for s in suspects if s.susNum == suspect_num), None)

                if not selected_suspect:
                    print("Invalid suspect number!")
                    continue

                try:
                    response = requests.get(selected_suspect.image)
                    response.raise_for_status()  # Raises an error for bad responses (404, 403, etc.)
                    img = Image.open(BytesIO(response.content))
                    img.show()
                except requests.exceptions.RequestException as e:
                    print(f"Failed to load image: {e}")
            except ValueError:
                print("Invalid input! Enter a number.")


            



suspectNum=1
points = 10
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
                image_url = "No image available"
                if "images" in item and isinstance(item["images"], list) and len(item["images"]) > 0:
                    image_url = item["images"][0].get("original", "No image available")
    
                suspect = Suspect(
                    name=item.get("title", "Unknown"),
                    crime=item.get("description", "No description available"),
                    sex = item.get("sex") if item.get("sex") is not None else "Unknown",
                    age=item.get("age_max") or item.get("age_min") or -1, 
                    reward=item.get("reward_max", 0),
                    aliases=", ".join(item.get("aliases", []) or []),  
                    fieldOffice=", ".join(item.get("field_offices", []) or []),
                    susNum=suspectNum,
                    image=image_url)

                suspects.append(suspect)
                suspectNum = suspectNum+1
                                
            except ValidationError as err:
                print(err)

game(points, suspects)
