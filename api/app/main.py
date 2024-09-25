from fastapi import FastAPI

from routers import (
    bird_router as bird,
    user_router as user
)


app = FastAPI()
app.include_router(bird.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}