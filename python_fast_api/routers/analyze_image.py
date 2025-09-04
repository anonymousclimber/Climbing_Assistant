# Contains the endpoint and functionality for analyzing an image using a pre-trained model. 
from fastapi import APIRouter, File, UploadFile, Request, Response
import cv2
import numpy as np
router = APIRouter()


# Use UploadFile to work well with larger files such as images. They are stored in memory up to a space limit, then stored on disk. 
@router.post("/analyze_image", response_class=Response)
async def analyze_image(request: Request, file: UploadFile = File(...)):
    # Current place holder for business logic. 
    # Access the model from app.state and pass the uploaded file stream
    image_bytes = await file.read()
    decoded_image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8),cv2.IMREAD_COLOR)
    
    results = request.app.state.pose_estimator(decoded_image)
    annotated_image = results[0].plot()
    # Encode the (possibly annotated) image as JPEG using OpenCV to avoid imageio warnings
    success, encoded = cv2.imencode('.jpg', annotated_image)
    if not success:
        return Response("Failed to encode image", status_code=500)

    im_bytes = encoded.tobytes()
    headers = {'Content-Disposition': 'inline; filename="output.jpg"'}
    return Response(im_bytes, headers=headers, media_type='image/jpeg')
