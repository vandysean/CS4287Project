from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from cryptography.fernet import Fernet

from stream2fa.common.functions import decode_base64_image
from stream2fa.common.objects import templates
from stream2fa.common.constants import CIPHER_KEY
from stream2fa.api.models import StreamFrame, UserInfo, StreamTemplateInfo

import os

router = APIRouter()

async def _compare_passwords(*, username: str, hashed_password: str, app: str) -> bool:
    stored_hashed_password_bytes = '123pass'.encode('utf-8') # would fetch from database
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    cipher = Fernet(CIPHER_KEY.encode("utf-8"))
    return cipher.decrypt(stored_hashed_password_bytes) == cipher.decrypt(hashed_password_bytes)

@router.post("/user/pwd")
async def stream(user_info: UserInfo):
    username, password, app = user_info.username, user_info.password, user_info.app
    
    try:
        is_password_authorized = await _compare_passwords(username=username, hashed_password=password, app=app)
        status = 'success' if is_password_authorized else 'failure'
    except Exception as e:
        status = f'error => {repr(e)} - un={username}, pw={password}, app={app}'
    
    return {'status': status}
    

@router.post("/user/stream")
async def stream(stream_frame: StreamFrame):
    try:
        img = await decode_base64_image(stream_frame.uri)
        status = 'success/failure'
    except Exception as e:
        status = f'error => {repr(e)}'
    
    ## Do thing with the image here ##
    
    return {'status': status}


@router.post("/user/stream/template", response_class=HTMLResponse)
async def stream_template(request: Request, stream_template_info: StreamTemplateInfo):
    template_data = {
        'request': request,
        'username': stream_template_info.username,
        'app': stream_template_info.app,
        'success_url': stream_template_info.success_url,
        'failure_url': stream_template_info.failure_url
    }
    
    return templates.TemplateResponse('auth_stream_template.html', template_data)
