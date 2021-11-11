from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from stream2fa.common.objects import templates
from stream2fa.api.models import RedirectTemplateInfo

router = APIRouter()

@router.post("/", response_class=HTMLResponse)
async def immediate_redirect(request: Request, redirect_template_info: RedirectTemplateInfo):
    template_data = {
        'request': request,
        'url': redirect_template_info.url
    }
    
    return templates.TemplateResponse('immediate_redirect.html', template_data)