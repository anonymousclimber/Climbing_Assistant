# Contains the endpoint and functionality for analyzing an image using a pre-trained model. 
from fastapi import APIRouter, File, UploadFile, Request
from typing import Annotated
router = APIRouter()


# Use UploadFile to work well with larger files such as images. They are stored in memory up to a space limit, then stored on disk. 
@router.post("/analyze_image")
async def analyze_image(request:Request, file:UploadFile):
    # Current place holder for business logic. 
    results = request.app.state.pose_estimator(file.file)
    for result in results:
        xy = result.keypoints.xy

    return {"filename":file.filename}
