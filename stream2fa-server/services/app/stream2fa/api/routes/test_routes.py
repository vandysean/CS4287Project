from fastapi import APIRouter

from stream2fa.common.functions import decode_base64_image
from stream2fa.api.models import TestMessage, StreamFrame

router = APIRouter()

@router.post("/stream")
async def test_stream(stream_frame: StreamFrame):
    try:
        img = await decode_base64_image(stream_frame.uri)
    except Exception as e:
        return {'status': 'failed', 'message': f'{repr(e)}'}
    
    return {"status": "Processed", "shape": f"{img.shape}", "type": f"{type(img)}", 
            "user": stream_frame.username, "app": stream_frame.app}


@router.get("/get")
def test_get():
    return {"message": "Hello FastAPI + SSL"}


@router.post("/post")
def test_post(message: TestMessage):
    text = message.text
    author = message.author
    response = {"status": "message received", "text": text, "author": author}
    return response
