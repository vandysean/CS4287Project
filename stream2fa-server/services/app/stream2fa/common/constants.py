import os

MAX_NUM_ENCODINGS_SAVED = 15

with open(os.path.join(os.getcwd(), "db-uri.txt"), "r") as f:
    DB_URI = f.read().strip()

HOST_NAME = "stream2fa.com"
