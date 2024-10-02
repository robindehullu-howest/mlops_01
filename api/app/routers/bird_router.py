from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
import json
from api.app.schemas.bird import Bird
from sqlalchemy.orm import Session
from api.app.models.bird_model import Bird as BirdRepo

import torch
import urllib.request
from PIL import Image
from transformers import pipeline

router = APIRouter(
    prefix="/birds",
    tags=["Bird"],
    responses={404: {"Bird": "Not found"}},
)

repo = BirdRepo()

def read_birds_from_file(file_name: str):
    with open(file_name, "r") as file:
        birds_data = json.load(file)
    return [Bird(**bird) for bird in birds_data]

#birds = read_birds_from_file("birds.json")

@router.get("/")
async def get_birds():
    objects = repo.get_all()
    if objects is None:
        raise HTTPException(status_code=400, detail="Something went wrong here!")
    return objects

@router.get("/{bird_id}")
async def get_bird(bird_id: str):
    retreived_object = repo.get_by(id=bird_id)
    if retreived_object is None:
        raise HTTPException(status_code=400, detail="Something went wrong here!")
    return retreived_object
    
@router.post("/")
async def create_bird(bird: Bird):
    created_object = repo.create(bird)
    if created_object is None:
        raise HTTPException(status_code=400, detail="Something went wrong here!")
    return created_object

@router.post("/classify")
async def classify_bird(img: UploadFile = File(...)):
    image = Image.open(img.file)
    pipe = pipeline("image-classification", model="dennisjooo/Birds-Classifier-EfficientNetB2")
    return pipe(image)[0]