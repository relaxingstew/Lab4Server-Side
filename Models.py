from pydantic import BaseModel
    
class Suspect(BaseModel):
    name: str
    crime: str
    sex: str
    age: int
    reward: int
    aliases: str
    fieldOffice: str
    susNum: int
    image:str

    def __repr__(self):
        return f"{self.name}"
    
class Crime(BaseModel):
    suspect: Suspect
    susNum:int
    crime: str
    crimNum:int = None
    isExtended:bool
    
    class Config:
        arbitrary_types_allowed = True
        
    @property
    def susNum(self):
        return self.suspect.susNum
    def crime(self):
        return self.suspect.crime
