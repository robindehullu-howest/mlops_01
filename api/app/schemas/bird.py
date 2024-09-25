from typing import Optional
from pydantic import BaseModel

class Bird(BaseModel):
    uuid: Optional[str] = None
    id: str
    name: str
    short: str
    image: str
    recon: list
    food: dict
    see: str

    def sayHello(self):
        return f"Hello {self.name}!"