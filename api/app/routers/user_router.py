from fastapi import APIRouter
from api.app.schemas.user import User

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"User": "Not found"}},
)

users = []

user = User(
    uuid="550e8400-e29b-41d4-a716-446655440000",
    name="John Doe",
    locationOfResidence="USA",
    age=50,
    gender="M",
    registrationDate="2021-01-01"
)

users.append(user)

@router.get("/users")
async def get_users():
    return users

@router.post("/users")
async def create_user(user: User):
    users.append(user)
    return user