from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from stream2fa.common.functions import decode_base64_image
from stream2fa.common.objects import templates
from stream2fa.api.models import StreamFrame, UserInfo, StreamTemplateInfo
from stream2fa.users.models import User


router = APIRouter()

@router.post("/user/pwd")
async def password_authorization(user_info: UserInfo):
    user = await User(user_info.username)
    
    try:
        is_password_authorized = await user.check_password(user_info.password)
        status = 'success' if is_password_authorized else 'failure'
    except Exception as e:
        status = f'error => {repr(e)}'
    
    return {'status': status}
    

@router.post("/user/stream")
async def stream_authorization(stream_frame: StreamFrame):
    user = await User(stream_frame.username)
    
    try:
        img = await decode_base64_image(stream_frame.uri)

        status = user.check_face_encodings(img)
    except Exception as e:
        status = f'error => {repr(e)}'
        
    return {'status': status}


@router.post("/user/stream/template", response_class=HTMLResponse)
async def authorization_stream_template(request: Request, stream_template_info: StreamTemplateInfo):
    template_data = {
        'request': request,
        'username': stream_template_info.username,
        'app': stream_template_info.app,
        'success_url': stream_template_info.success_url,
        'failure_url': stream_template_info.failure_url,
        'js_file': 'auth-stream.js'
    }
    
    return templates.TemplateResponse('stream_template.html', template_data)
