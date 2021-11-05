from pydantic import BaseModel

class TestMessage(BaseModel):
    text: str
    author: str

class StreamFrame(BaseModel):
    uri: str
    username: str
    password: str
    app: str

