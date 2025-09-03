from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import analyze_image
from ultralytics import YOLO

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Loading the machine Learning model. 
    # Initializes the YOLO pose estimation model. 
    app.pose_estimator = YOLO("yolo11n-pose.pt")
    yield


# Creating the actual FASTAPI app instance
app = FastAPI(lifespan=lifespan)
app.include_router(analyze_image.router)

@app.get("/")
def read_root():
    return "Welcome to Image Analysis."

