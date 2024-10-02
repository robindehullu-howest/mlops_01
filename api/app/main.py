from fastapi import FastAPI
from api.app.models.bird_model import Bird
from api.app.models.user_model import User
from api.app.routers import bird_router as bird, user_router as user
import api.app.database as db
from api.app.gradio_interface import create_gradio_interface

db.start_db()

app = FastAPI()

app.include_router(bird.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

demo = create_gradio_interface()
demo.launch(server_name="0.0.0.0", server_port=7860, prevent_thread_lock=True)