from fastapi import APIRouter
import json
from api.app.schemas.bird import Bird

router = APIRouter(
    prefix="/birds",
    tags=["Bird"],
    responses={404: {"Bird": "Not found"}},
)

def read_birds_from_file(file_name: str):
    with open(file_name, "r") as file:
        birds_data = json.load(file)
    return [Bird(**bird) for bird in birds_data]

birds = read_birds_from_file("birds.json")

@router.get("/")
async def get_birds():
    return birds

@router.get("/{bird_id}")
async def get_bird(bird_id: str):
    for bird in birds:
        if bird.id == bird_id:
            return bird

    return {"message": "Bird not found"}