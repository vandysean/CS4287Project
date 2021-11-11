from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from stream2fa.common.functions import decode_base64_image
from stream2fa.common.objects import templates
from stream2fa.api.models import StreamFrame, UserInfo, StreamTemplateInfo

import face_recognition as fr
import os

router = APIRouter()

async def _compare_passwords(username: str, hashed_password: str, app: str) -> bool:
    # get password from db and compare to passed password
    
    return True #  unhashed_stored_password == unhashed_password

@router.post("/user/pwd")
async def password_authorization(user_info: UserInfo):
    username, password, app = user_info.username, user_info.password, user_info.app
    
    try:
        is_password_authorized = await _compare_passwords(username, password, app)
        status = 'success' if is_password_authorized else 'failure'
    except Exception as e:
        status = f'error => {repr(e)}'
    
    return {'status': status}
    

@router.post("/user/stream")
async def stream_authorization(stream_frame: StreamFrame):
    try:
        img = await decode_base64_image(stream_frame.uri)
        face_locations = fr.face_locations(img)
        face_encodings = fr.face_encodings(img, face_locations)

        known_img = fr.load_image_file(os.path.join(os.getcwd(), "test.jpg"))
        known_encoding = fr.face_encodings(known_img)[0]
        # status = 'ongoing' # ongoing / success

        matches = fr.compare_faces(face_encodings, known_encoding)
        status = 'success' if True in matches else 'ongoing'
    except Exception as e:
        status = f'error => {repr(e)}'
    
    ## Do thing with the image here ##
    
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
