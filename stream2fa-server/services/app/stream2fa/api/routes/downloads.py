from fastapi import APIRouter
from fastapi.responses import FileResponse

import os

router = APIRouter()

@router.get('/{file_name}', response_class=FileResponse)
def download_file(file_name: str):
    file_type = file_name.split('.')[1]
    
    if file_type == 'js' or file_type == 'css':
        return os.path.join(os.getcwd(), 'stream2fa', 'static', file_type, file_name)
    else:
        return os.path.join(os.getcwd(), 'stream2fa', 'static', 'misc', file_name)
        