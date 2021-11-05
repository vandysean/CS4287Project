from fastapi import APIRouter
import cv2
import numpy as np
import base64

from stream2fa.models.test_models import TestMessage
from stream2fa.models.test_models import StreamFrame

router = APIRouter()

async def decode_base64_image(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img


@router.post("/stream")
async def stream(stream_frame: StreamFrame):
    img = await decode_base64_image(stream_frame.uri)
    return {"status": "Processed", "shape": f"{img.shape}", "type": f"{type(img)}", "user": stream_frame.username, "pass": stream_frame.password, "app": stream_frame.app}


@router.get("/get")
def hello():
    return {"message": "Hello FastAPI + SSL"}


@router.post("/post")
def send_message(message: TestMessage):
    text = message.text
    author = message.author
    response = {"status": "message received", "text": text, "author": author}
    return response
