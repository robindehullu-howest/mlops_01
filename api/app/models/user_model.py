from api.app.database import Base
from sqlalchemy import Column, Integer, String
from api.app.schemas.user import User
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    uuid = Column(String(36), default=generate_uuid(), primary_key=True, index=True)
    name = Column(String(50))
    locationOfResidence = Column(String(50))
    age = Column(Integer)
    gender = Column(String(10))
    registrationDate = Column(String(50))

#    def __init__(self, user: User):
#        self.uuid = user.uuid if user.uuid is not None else generate_uuid()
#        self.name = user.name
#        self.locationOfResidence = user.locationOfResidence
#        self.age = user.age
#        self.gender = self.gender
#        self.registrationDate = user.registrationDate