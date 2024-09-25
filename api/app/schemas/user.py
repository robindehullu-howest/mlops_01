from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    uuid: str
    name: str
    locationOfResidence: str
    age: int
    gender: str
    registrationDate: str

    def sayHello(self):
        return f"Hello {self.name}!"
