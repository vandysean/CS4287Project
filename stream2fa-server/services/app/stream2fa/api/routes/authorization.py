from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from stream2fa.common.functions import decode_base64_image
from stream2fa.common.objects import templates
from stream2fa.api.models import StreamFrame, UserInfo, StreamTemplateInfo


router = APIRouter()

async def _compare_passwords(*, username: str, hashed_password: str, app: str) -> bool:
    # get password from db and compare to passed password
    
    return True #  unhashed_stored_password == unhashed_password

@router.post("/user/pwd")
async def stream(user_info: UserInfo):
    username, password, app = user_info.username, user_info.password, user_info.app
    
    try:
        is_password_authorized = await _compare_passwords(username=username, hashed_password=password, app=app)
        status = 'success' if is_password_authorized else 'failure'
    except Exception as e:
        status = f'error => {repr(e)}'
    
    return {'status': status}
    

@router.post("/user/stream")
async def stream(stream_frame: StreamFrame):
    try:
        img = await decode_base64_image(stream_frame.uri)
    except Exception as e:
        return {'status': f'error => {repr(e)}'}
    
    ## Do thing with the image here ##
    
    return {'status': 'success/failure'}


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
