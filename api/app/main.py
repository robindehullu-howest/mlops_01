from fastapi import FastAPI
import json

from schemas.bird import Bird
from schemas.user import User

app = FastAPI()

def read_birds_from_file(file_name: str):
    with open(file_name, "r") as file:
        birds_data = json.load(file)
    return [Bird(**bird) for bird in birds_data]

birds = read_birds_from_file("birds.json")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/birds")
async def get_birds():
    return birds