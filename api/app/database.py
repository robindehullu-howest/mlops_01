import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# This will get our environment variables, or some fallback values. But remember that these won't work as the .env file was included for the database
MYSQL_USER = os.getenv('MYSQL_USER', 'user')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'birds_db')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'user_password')

engine = create_engine(
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
)
session = sessionmaker(autoflush=False, bind=engine)

db = session()
Base = declarative_base()

def start_db():
    Base.metadata.create_all(engine)