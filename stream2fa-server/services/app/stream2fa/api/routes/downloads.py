from fastapi import APIRouter
from fastapi.responses import FileResponse

import os

router = APIRouter()

@router.get('/', response_class=FileResponse)
def download(file_name: str):
    file_type = 'js' if file_name.split('.')[1] == 'js' else 'css'
    
    return os.path.join(os.getcwd(), 'stream2fa', 'static', file_type, file_name)
        