import requests
from pydantic import ValidationError
import json
from Models import Suspect, Crime
import random
import re
def regCrimes(crim):
    semi =crim.split(';', 3)
    if len(semi) >= 3:
        return ';'.join(semi[:3])
    else:
        return crim

def crimMenu(crim):
    while true:
        for crime in crim:
            print(f"{crime.crime}")
def susMenu():
    print("")
def matchMenu():
    print("")
def game(num, sus, crim):
    while True:
        userInp = input(f"Current Points|{num}| Enter [S]uspects [I]nspect [C]rimes [Q]uit or [M]ake a guess:\n")
        userInp = userInp.lower()
        if userInp == "s":
            for suspect in sus:
                print(f"Suspect {suspect.susNum} {suspect.name}")    
        if userInp == "c":
            num2 = 1
            for crime in crim:
                print(f"{num2}. - {regCrimes(crime.crime)}  \n")
                num2=num2+1
        if userInp == "i":
            for suspect in sus:
                inp = input("Enter [S]uspects or [C]rimes")
                inp = inp.lower()
           ##     if in
        

            



suspectNum=1
points = 10
fbi_url = "https://api.fbi.gov/wanted/v1/list"
num = random.randint(2,48)
suspects = []
crimes = []

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
                crime = Crime(
                    crime = suspect.crime,
                    crimNum = 0,
                    susNum = suspect.susNum,
                    suspect = suspect
                )
                crimes.append(crime)
                suspects.append(suspect)
                suspectNum = suspectNum+1
                                
            except ValidationError as err:
                print(err)

temp = 1
random.shuffle(crimes)
for crime in crimes:
    crime.crimNum = temp
    temp = temp+1
    
game(points, suspects, crimes)
