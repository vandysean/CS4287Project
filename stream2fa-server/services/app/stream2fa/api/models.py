from pydantic import BaseModel

class TestMessage(BaseModel):
    text: str
    author: str

class StreamFrame(BaseModel):
    uri: str
    username: str
    app: str
    
class AppReg(BaseModel):
    app: str
    
class UserRegInit(BaseModel):
    username: str
    password: str
    app: str
    
class UserAuthInit(BaseModel):
    username: str
    password: str
    app: str
