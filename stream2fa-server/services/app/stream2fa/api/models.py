from pydantic import BaseModel

class TestMessage(BaseModel):
    text: str
    author: str

class StreamFrame(BaseModel):
    uri: str
    username: str
    app: str
    
class AppInfo(BaseModel):
    app: str
    
class UserInfo(BaseModel):
    username: str
    password: str
    app: str
    
class StreamTemplateInfo(BaseModel):
    username: str
    app: str
    success_url: str
    failure_url: str
    
class RedirectTemplateInfo(BaseModel):
    url: str
