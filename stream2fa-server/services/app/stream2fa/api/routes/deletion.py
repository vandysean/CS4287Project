from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from stream2fa.api.models import DeleteUserInfo


router = APIRouter()

@router.delete('/user')
async def stream(delete_user_info: DeleteUserInfo):
    username, app = delete_user_info.username, delete_user_info.app
    
    try:
        # delete the user from database
        status = 'success'
    except Exception as e:
        status = f'error => {repr(e)}'
    
    return {'status': status}
