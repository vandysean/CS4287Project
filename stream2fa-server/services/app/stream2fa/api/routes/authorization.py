from fastapi import APIRouter

from stream2fa.common.functions import decode_base64_image
from stream2fa.api.models import StreamFrame, UserAuthInit

import traceback

router = APIRouter()

@router.post("/user/init")
async def stream(user_info: UserAuthInit):
    username, password, app = user_info.username, user_info.password, user_info.app
    
    ## Dehash password, see if it belongs to $username within $app ##
    try:
        status = 'completed'
    except Exception as e:
        status = f'error => {traceback.format_exception(e)}'
    
    return {'status': status}
    

@router.post("/user/stream")
async def stream(stream_frame: StreamFrame):
    try:
        img = await decode_base64_image(stream_frame.uri)
        status = 'success/failure'
    except Exception as e:
        status = f'error => {traceback.format_exception(e)}'
    
    ## Do thing with the image here ##
    
    return {'status': status}

