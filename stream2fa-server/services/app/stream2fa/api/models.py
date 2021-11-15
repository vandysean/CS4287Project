from pydantic import BaseModel

class StreamFrame(BaseModel):
    uri: str
    username: str
    
class UserInfo(BaseModel):
    username: str
    password: str
    
class DeleteUserInfo(BaseModel):
    username: str
    
class StreamTemplateInfo(BaseModel):
    username: str
    success_url: str
    failure_url: str
    
class RedirectTemplateInfo(BaseModel):
    url: str

