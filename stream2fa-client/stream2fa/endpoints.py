
BASE_ENDPOINT = 'http://35.153.43.136:8000'

USER_PWD_AUTH_ENDPOINT = '/'.join([BASE_ENDPOINT, 'auth', 'user', 'pwd'])

USER_PWD_REG_ENDPOINT = '/'.join([BASE_ENDPOINT, 'register', 'user', 'pwd'])

IMMEDIATE_REDIRECT_ENDPOINT = '/'.join([BASE_ENDPOINT, 'redirect'])

GET_AUTH_STREAM_TEMPLATE_ENDPOINT = '/'.join([BASE_ENDPOINT, 'auth', 'user', 'stream', 'template'])
GET_REG_STREAM_TEMPLATE_ENDPOINT = '/'.join([BASE_ENDPOINT, 'register', 'user', 'stream', 'template'])

DELETE_USER_ENDPOINT = '/'.join([BASE_ENDPOINT, 'delete', 'user'])
