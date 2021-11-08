from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from stream2fa.common.constants import MAX_NUM_ENCODINGS_SAVED
from stream2fa.common.functions import decode_base64_image
from stream2fa.common.objects import templates
from stream2fa.api.models import StreamFrame, AppInfo, UserInfo, StreamTemplateInfo

router = APIRouter()

@router.post("/user/pwd")
async def stream(user_info: UserInfo):
    username, password, app = user_info.username, user_info.password, user_info.app
    
    ## Check if username is available, if so create new user in db ##
    try:
        status = 'success'  # success / failure
    except Exception as e:
        status = f'error => {repr(e)}'
    
    return {'status': status}

@router.post("/user/stream")
async def stream(stream_frame: StreamFrame):
    try:
        img = await decode_base64_image(stream_frame.uri)
        status = 'ongoing'  # ongoing / complete / failed
    except Exception as e:
        status = f'error => {repr(e)}'
    
    ## Do thing with the image here ##
    num_encodings_saved = MAX_NUM_ENCODINGS_SAVED - 1 # get this number from above logic somehow
    
    return {'status': status,
            'encodings_saved': num_encodings_saved,
            'max_encodings_saved': MAX_NUM_ENCODINGS_SAVED}

@router.post("/user/stream/template", response_class=HTMLResponse)
async def stream_template(request: Request, stream_template_info: StreamTemplateInfo):
    template_data = {
        'request': request,
        'username': stream_template_info.username,
        'app': stream_template_info.app,
        'success_url': stream_template_info.success_url,
        'failure_url': stream_template_info.failure_url,
        'js_file': 'reg-stream.js'
    }
    
    return templates.TemplateResponse('stream_template.html', template_data)
