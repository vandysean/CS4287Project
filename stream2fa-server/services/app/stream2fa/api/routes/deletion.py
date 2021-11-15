from fastapi import APIRouter

from stream2fa.api.models import DeleteUserInfo
from stream2fa.users.models import User

router = APIRouter()

@router.delete('/user')
async def delete_user(delete_user_info: DeleteUserInfo):
    user = User(delete_user_info.username)

    try:
        res = await user.delete()

        status = res['message']
    except Exception as e:
        status = f'error => {repr(e)}'
    
    return {'status': status}

