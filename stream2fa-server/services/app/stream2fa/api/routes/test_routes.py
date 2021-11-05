from fastapi import APIRouter

from stream2fa.common.functions import decode_base64_image
from stream2fa.api.models import TestMessage, StreamFrame

router = APIRouter()

@router.post("/stream")
async def stream(stream_frame: StreamFrame):
    img = await decode_base64_image(stream_frame.uri)
    return {"status": "Processed", "shape": f"{img.shape}", "type": f"{type(img)}", 
            "user": stream_frame.username, "pass": stream_frame.password,
            "app": stream_frame.app}


@router.get("/get")
def hello():
    return {"message": "Hello FastAPI + SSL"}


@router.post("/post")
def send_message(message: TestMessage):
    text = message.text
    author = message.author
    response = {"status": "message received", "text": text, "author": author}
    return response
