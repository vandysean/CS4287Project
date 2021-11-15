from stream2fa.endpoints import (
    USER_PWD_AUTH_ENDPOINT,
    IMMEDIATE_REDIRECT_ENDPOINT,
    GET_AUTH_STREAM_TEMPLATE_ENDPOINT
)

import requests
import json
import hashlib


def authorize_user(*, username: str, password: str, app: str, success_url: str, failure_url: str) -> str:
    hash_function = hashlib.new('sha512_256').update(password.encode('utf-8'))
    hashed_password = hash_function.hexdigest()
        
    pwd_auth_data = {'username': username, 'password': hashed_password, 'app': app}
    pwd_auth_response = requests.post(USER_PWD_AUTH_ENDPOINT, data=json.dumps(pwd_auth_data)).json()
        
    if pwd_auth_response['status'] == 'success':
        stream_auth_data = {'username': username, 'app': app, 'success_url': success_url, 'failure_url': failure_url}
        stream_auth_response = requests.post(GET_AUTH_STREAM_TEMPLATE_ENDPOINT, data=json.dumps(stream_auth_data))
        
        return stream_auth_response.text
    else:
        redirect_data = {'url': failure_url}
        redirect_response = requests.post(IMMEDIATE_REDIRECT_ENDPOINT, data=json.dumps(redirect_data)) 
        
        return redirect_response.text
