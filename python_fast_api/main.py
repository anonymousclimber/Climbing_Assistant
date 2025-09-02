from typing import Union

from fastapi import FastAPI
from .routers import analyze_image

app = FastAPI()
app.include_router(analyze_image.router)

@app.get("/")
def read_root():
    return "Welcome to Image Analysis."

