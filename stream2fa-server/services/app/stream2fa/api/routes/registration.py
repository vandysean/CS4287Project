from fastapi import APIRouter

from stream2fa.common.functions import decode_base64_image
from stream2fa.api.models import StreamFrame, AppReg, UserRegInit

import traceback

router = APIRouter()

@router.post("/app")
async def stream(app_info: AppReg):
    app = AppReg.app
    
    ## Check if app with this name exists in db already, if not create one in db ##
    try:
        status = 'completed'
    except Exception as e:
        status = f'error => {traceback.format_exception(e)}'
    
    return {'status': status}

@router.post("/user/init")
async def stream(user_info: UserRegInit):
    username, password, app = user_info.username, user_info.password, user_info.app
    
    ## Check if username is available, if so create new user in db ##
    try:
        status = 'completed'
    except Exception as e:
        status = f'error => {traceback.format_exception(e)}'
    
    return {'status': status}

@router.post("/user/stream")
async def stream(stream_frame: StreamFrame):
    try:
        img = await decode_base64_image(stream_frame.uri)
        status = 'ongoing/completed'
    except Exception as e:
        status = f'error => {traceback.format_exception(e)}'
    
    ## Do thing with the image here ##
    
    return {'status': status}
