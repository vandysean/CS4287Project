import requests
import json
import hashlib
from stream2fa.endpoints import (
    USER_PWD_REG_ENDPOINT,
    USER_PWD_AUTH_ENDPOINT,
    IMMEDIATE_REDIRECT_ENDPOINT,
    GET_AUTH_STREAM_TEMPLATE_ENDPOINT,
    GET_REG_STREAM_TEMPLATE_ENDPOINT,
    DELETE_USER_ENDPOINT
)


def register_user(*, username: str, password: str, success_url: str, failure_url: str) -> str:
    hash_function = hashlib.new('sha512_256').update(password.encode('utf-8'))
    hashed_password = hash_function.hexdigest()
    
    pwd_reg_data = {'username': username, 'password': hashed_password}
    pwd_reg_response = requests.post(USER_PWD_REG_ENDPOINT, data=json.dumps(pwd_reg_data)).json()
        
    if pwd_reg_response['status'] == 'success':
        stream_reg_data = {'username': username, 'success_url': success_url, 'failure_url': failure_url}
        stream_reg_response = requests.post(GET_REG_STREAM_TEMPLATE_ENDPOINT, data=json.dumps(stream_reg_data))
        
        return stream_reg_response.text
    else:
        redirect_data = {'url': failure_url}
        redirect_response = requests.post(IMMEDIATE_REDIRECT_ENDPOINT, data=json.dumps(redirect_data)) 
        
        return redirect_response.text
    
    
def authorize_user(*, username: str, password: str, success_url: str, failure_url: str) -> str:
    hash_function = hashlib.new('sha512_256').update(password.encode('utf-8'))
    hashed_password = hash_function.hexdigest()
        
    pwd_auth_data = {'username': username, 'password': hashed_password}
    pwd_auth_response = requests.post(USER_PWD_AUTH_ENDPOINT, data=json.dumps(pwd_auth_data)).json()
        
    if pwd_auth_response['status'] == 'success':
        stream_auth_data = {'username': username, 'success_url': success_url, 'failure_url': failure_url}
        stream_auth_response = requests.post(GET_AUTH_STREAM_TEMPLATE_ENDPOINT, data=json.dumps(stream_auth_data))
        
        return stream_auth_response.text
    else:
        redirect_data = {'url': failure_url}
        redirect_response = requests.post(IMMEDIATE_REDIRECT_ENDPOINT, data=json.dumps(redirect_data)) 
        
        return redirect_response.text
    
    
def delete_user(*, username: str) -> None:
    user_delete_data = {'username': username}
    requests.delete(DELETE_USER_ENDPOINT, data=json.dumps(user_delete_data))

