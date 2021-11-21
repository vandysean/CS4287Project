from fastapi import APIRouter, Form, Request, Depends
from fastapi.security import APIKeyCookie
from starlette.responses import RedirectResponse, Response, HTMLResponse
from jose import jwt

from stream2fa import client as stream2fa
from stream2fa.common.objects import templates
from stream2fa.common.constants import HOST_NAME
from stream2fa.common.constants import SECRET_KEY

router = APIRouter()

cookie_sec = APIKeyCookie(name="session", auto_error=False)
        

@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup", response_class=HTMLResponse)
async def signup(username: str = Form(...), password: str = Form(...)):
    success_url = router.url_path_for('dashboard_redirect', username=username)
    failure_url = router.url_path_for('home')
    
    return HTMLResponse(stream2fa.register_user(username=username, password=password,
                                   success_url=success_url, failure_url=failure_url))


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, session: str = Depends(cookie_sec)):       
    if session:
        return RedirectResponse(router.url_path_for("dashboard"))
    else:
        return templates.TemplateResponse("login.html", {"request": request})        


@router.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    success_url = router.url_path_for('dashboard_redirect', username)
    failure_url = router.url_path_for('home')
    
    return HTMLResponse(stream2fa.register_user(username=username, password=password,
                                   success_url=success_url, failure_url=failure_url))


@router.get("/dashboard/redirect/{username}", response_class=RedirectResponse)
async def dashboard_redirect(request: Request, response: Response,
                             username: str, session: str = Depends(cookie_sec)):
    
    if request.url.hostname != HOST_NAME:
        return RedirectResponse(router.url_path_for("home"))
    
    if not session:
        token = jwt.encode({"username": username}, SECRET_KEY)        
        response.set_cookie("session", token)
    
    return RedirectResponse(router.url_path_for("dashboard"))
    
    
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session: str = Depends(cookie_sec)):   
    if session:
        template_parameters = {
            "request": request,
            "username": jwt.decode(session, SECRET_KEY)["username"]
        }
        
        return templates.TemplateResponse("dashboard.html", template_parameters)
    else:
        return RedirectResponse(router.url_path_for("home"))
        

@router.get("/logout", response_class=RedirectResponse)
async def logout(request: Request, response: Response, session: str = Depends(cookie_sec)):    
    if not session:
        return RedirectResponse(url=str(request.url))
    
    ret = RedirectResponse(router.url_path_for('home'))
    
    response.delete_cookie("session")
    
    return ret

@router.get('/delete', response_class=RedirectResponse)
async def delete(request: Request, response: Response, session: str = Depends(cookie_sec)):
    if not session:
        return RedirectResponse(url=str(request.url))
    
    payload = jwt.decode(session, SECRET_KEY)
    stream2fa.delete_user(username=payload['username'])
    
    ret = RedirectResponse(router.url_path_for('home'))
    
    response.delete_cookie("session")
    
    return ret
