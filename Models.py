from pydantic import BaseModel

class Suspect(BaseModel):
    name: str
    crime: str
    sex: str
    age: int
    reward: int
    aliases: str
    fieldOffice: str

    def __repr__(self):
        return f"{self.name}"
