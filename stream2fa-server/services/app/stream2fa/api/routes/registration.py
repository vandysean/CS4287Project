from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from stream2fa.common.constants import MAX_NUM_ENCODINGS_SAVED
from stream2fa.common.functions import decode_base64_image
from stream2fa.common.objects import templates
from stream2fa.api.models import StreamFrame, UserInfo, StreamTemplateInfo
from stream2fa.users.models import User

router = APIRouter()

@router.post("/user/pwd")
async def password_registration(user_info: UserInfo):    
    user = User()
    
    try:
        res = await user.signup(user_info.username, user_info.password)
        if res['message'] == 'success':
            status = 'success'  # success / failure
        else:
            status = 'failure'
        
        print(res['message'])
    except Exception as e:
        status = f'error => {repr(e)}'
    
    return {'status': status}

@router.post("/user/stream")
async def stream_registration(stream_frame: StreamFrame):
    user = User(stream_frame.username)

    num_encodings_saved = 0    
    try:
        img = await decode_base64_image(stream_frame.uri)
        
        res = await user.update_face_encodings(img)
        print(res)        
        status = res['message']
        num_encodings_saved = res['num_saved']
        
        
    except Exception as e:
        print("Error:", repr(e))
        status = f'error => {repr(e)}'
        
    return {'status': status,
            'encodings_saved': num_encodings_saved,
            'max_encodings_saved': MAX_NUM_ENCODINGS_SAVED}

@router.post("/user/stream/template", response_class=HTMLResponse)
async def registration_stream_template(request: Request, stream_template_info: StreamTemplateInfo):
    template_data = {
        'request': request,
        'username': stream_template_info.username,
        'app': stream_template_info.app,
        'success_url': stream_template_info.success_url,
        'failure_url': stream_template_info.failure_url,
        'js_file': 'reg-stream.js'
    }
    
    return templates.TemplateResponse('stream_template.html', template_data)
