from fastapi.templating import Jinja2Templates
import pymongo
import ssl

from stream2fa.common.constants import DB_URI

templates = Jinja2Templates(directory="stream2fa/templates")

# client = pymongo.MongoClient(DB_URI, ssl_cert_reqs=ssl.CERT_NONE)
# db = client.user_login_system
db = pymongo.MongoClient(DB_URI, ssl_cert_reqs=ssl.CERT_NONE).user_login_system
