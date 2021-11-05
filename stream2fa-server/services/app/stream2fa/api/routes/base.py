from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from stream2fa.common.objects import templates

router = APIRouter()

@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})