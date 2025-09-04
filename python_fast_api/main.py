from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import analyze_image
from ultralytics import YOLO

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Loading the machine Learning model. 
    # Initializes the YOLO pose estimation model. 
    app.state.pose_estimator = YOLO("yolo11n-pose.pt")
    yield


# Creating the actual FASTAPI app instance
app = FastAPI(lifespan=lifespan)
app.include_router(analyze_image.router)

# Mount static assets and serve the frontend
app.mount("/static", StaticFiles(directory="python_fast_api/static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("python_fast_api/static/index.html")

