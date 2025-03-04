import requests
from pydantic import ValidationError
import json
from Models import Suspect, Crime
import random
import re

def bonusCrime(crime):
    tokens = crime.crime.split(';')
    
    if crime.isExtended == True and len(tokens) > 4:
        return tokens[4]
    if crime.isExtended == False and len(tokens) > 2:
        return tokens[2]
    else:
        return "Not enough are listed"
        
def regCrimes(crim, num):
    if crim.isExtended:
        num +=2
    semi =crim.crime.split(';')
    return ';'.join(semi[:num]) if num <= len(semi) else crim.crime
def crimMenu(crim):
   print("")
def susMenu(sus):
    for suspect in sus:
        print(f"{suspect.susNum} {suspect.name}")
    usrInp = input("Enter a suspect number: ")
    
def matchMenu():
    print("")

def game(num, sus, crim):
    regCrim = 2
    while num > 0:
        userInp = input(f"Current Points|{num}| Enter [S]uspects [I]nspect [C]rimes [Q]uit or [M]ake a guess:\n")
        userInp = userInp.lower()
        if userInp == "s":
            for suspect in sus:
                print(f"Suspect {suspect.susNum} {suspect.name}")    
        if userInp == "c":
            for crime in crim:
                print(f"{crime.crimNum}. - {regCrimes(crime, regCrim)}")
        if userInp == "i":
            inp = input("Enter [S]uspects or [C]rimes: ")
            inp = inp.lower()

            if inp == "s":
                for suspect in sus:
                    print(f"Suspect {suspect.susNum} {suspect.name}")
                inp = input("Enter suspect to reveal a crime that they may have committed(3 Points)")
                for crime in crim:
                    if int(inp) == crime.susNum:
                        print(bonusCrime(crime))
                    
                
            elif inp == "c":
                for crime in crim:
                    print(f"{crime.crimNum}. - {regCrimes(crime, regCrim)}")
                inp = input("Select a [C]rime or [P]ay 7 points to extend all crimes by 2: ")
                inp = inp.lower()
                if inp == "c":
                    inp = input ("Enter a crime to pay 2 points to extend: ")
                    for crime in crim:
                        if crime.crimNum == inp:
                            crime.isExtended = True
                    num = num - 2
                if inp == "p":
                    for crime in crim:
                        crime.isExtended = True
                    num = num - 7
                                
                                
        if userInp == "m":
            susGuess = None
            crimGuess = None
            for suspect in sus:
                print(f"Suspect {suspect.susNum} {suspect.name}")
            susGuess = int(input("Enter Suspect Number: "))
            suss = None
            for suspect in sus:
                if susGuess == suspect.susNum:
                    suss = suspect
            for crime in crim:
                print(f"{crime.crimNum}. - {regCrimes(crime, regCrim)}")
            crimGuess = int(input("Enter Crime Number: "))
            crimm = None
            for crime in crim:
                if crimGuess == crime.crimNum:
                    crimm = crime

            if crimm.susNum == suss.susNum:
                print("correct")
                num = num + 3
                sus.remove(suss)
                crim.remove(crimm)
            else:
                print("incorrect")
                num = num - 1 
            



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
                    suspect = suspect,
                    isExtended = False
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
sorted(crimes, key=lambda x: x.crimNum, reverse=True)

game(points, suspects, crimes)
print("Game Over")
