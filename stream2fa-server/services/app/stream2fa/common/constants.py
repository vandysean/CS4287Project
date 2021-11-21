import secrets

MAX_NUM_ENCODINGS_SAVED = 15

DB_URI = "mongodb+srv://admin:IpjsuXtcjy0Bmz6G@cluster0.6m2dg.mongodb.net/Cluster0?retryWrites=true&w=majority"

HOST_NAME = "stream2fa.com"

SECRET_KEY = secrets.token_hex(32)
