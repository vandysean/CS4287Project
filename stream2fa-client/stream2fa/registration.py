from stream2fa.endpoints import (
    USER_PWD_REG_ENDPOINT,
    IMMEDIATE_REDIRECT_ENDPOINT,
    GET_REG_STREAM_TEMPLATE_ENDPOINT
)

import requests
import json


def register_user(*, username: str, password: str, app: str, success_url: str, failure_url: str) -> str:
    hashed_password = password  # do whatever hashing/encryption here
    
    pwd_reg_data = {'username': username, 'password': hashed_password, 'app': app}
    pwd_reg_response = requests.post(USER_PWD_REG_ENDPOINT, data=json.dumps(pwd_reg_data)).json()
        
    if pwd_reg_response['status'] == 'success':
        stream_reg_data = {'username': username, 'app': app, 'success_url': success_url, 'failure_url': failure_url}
        stream_reg_response = requests.post(GET_REG_STREAM_TEMPLATE_ENDPOINT, data=json.dumps(stream_reg_data))
        
        return stream_reg_response.text
    else:
        redirect_data = {'url': failure_url}
        redirect_response = requests.post(IMMEDIATE_REDIRECT_ENDPOINT, data=json.dumps(redirect_data)) 
        
        return redirect_response.text
