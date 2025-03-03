from pydantic imprort BaseModel

class Suspect(BaseModel):
    name: str
    crime: str
    sex: str
    age: int
    reward: int
    aliases: str
    fieldOffice: str
