import uuid
from api.app.database import Base
from sqlalchemy import Column, Integer, String
from api.app.models.custom_types import TextPickleType
from api.app.database import Base, db
from api.app.schemas.bird import Bird as BirdSchema

def generate_uuid():
    code = str(uuid.uuid4())
    print(f"Generated UUID: {code}")
    return code

class Bird(Base):
    __tablename__ = 'birds'
    uuid = Column(String(36), default=generate_uuid(), primary_key=True, index=True)
    id = Column(String(50), index=True)
    name = Column(String(50), index=True)
    short = Column(String(250))
    image = Column(String(100))
    recon = Column(TextPickleType())
    food = Column(TextPickleType())
    see = Column(String(500))

    def __init__(self, *,
        uuid:str = generate_uuid(),
        id:str = '',
        name:str = '',
        short:str = '',
        image:str = '',
        recon:list = '',
        food:dict = '',
        see:str = ''
    ):
        self.uuid = uuid
        self.id = id
        self.name = name
        self.short = short
        self.image = image
        self.recon = recon
        self.food = food
        self.see = see

        self.model = Bird
        self.schema = BirdSchema

    def get_all(self):
        try:
            db_objects = db.query(self.model).all()
            if db_objects:
                return db_objects
            else:
                print(f"No {self.model} was found!")
                return None
        except Exception as e:
            print(f"Error while getting all {self.model}s.")
            print(e)
            db.rollback()

    def get_by(self, **kwargs):
        try:
            db_object = db.query(self.model).filter_by(**kwargs).first()
            if db_object:
                return db_object
            else:
                print(f"No {self.model} was found with {kwargs}!")
                return None
        except Exception as e:
            print(f"Error while getting {self.model}.")
            print(e)
            db.rollback()

    def get_many(self, **kwargs):
        try:
            db_objects = db.query(self.model).filter_by(**kwargs).all()
            if db_objects:
                return db_objects
            else:
                print(f"No {self.model} was found with {kwargs}!")
                return None
        except Exception as e:
            print(f"Error while getting {self.model}.")
            print(e)
            db.rollback()

    def create(self, obj: BirdSchema):
        try:
            obj_in_db = self.get_by(name=obj.name)
            if obj_in_db is None:
                new_obj = self.model(**obj.model_dump())
                db.add(new_obj)
                db.commit()

                print(f"{self.model} has been added to the database!")
                obj = self.schema.from_orm(new_obj)
            else:
                obj = None
                print(f"A {self.model} already exists.")

            return obj

        except Exception as e:
            print(f"Error while creating {self.model}.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()

    def update(self, new_obj: BirdSchema):
        try:
            old_obj = db.query(self.model).filter_by(uuid=new_obj.uuid).first()
            if old_obj:
                for key, value in new_obj.model_dump(exclude_unset=True).items():
                    setattr(old_obj, key, value)
                db.commit()
                print(f"{self.model} has been updated!")
            else:
                print(f"No {self.model} was found with uuid {new_obj.uuid}!")
        except Exception as e:
            print(f"Error while updating {self.model}.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()
            

    def delete(self, old_obj: BirdSchema):
        try:
            num_rows_deleted = db.query(self.model).filter_by(uuid=old_obj.uuid).delete()
            print(f"Number of {self.model}s deleted: {num_rows_deleted}")
            db.commit()
        except Exception as e:
            print(f"Error while deleting {self.model}.")
            print("Rolling back the database commit.")
            print(e)
            db.rollback()