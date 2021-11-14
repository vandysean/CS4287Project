from passlib.hash import pbkdf2_sha256
from stream2fa.common.objects import db
from stream2fa.common.constants import MAX_NUM_ENCODINGS_SAVED

import face_recognition
import numpy as np
import uuid


class User:
    user = None
    
    async def __init__(self, username=None):
        if username:
            self.user = db.users.find_one({
                "username": username
            })
            
            print(self.user)

    async def signup(self, username, password):
        # Create the user object
        self.user = {
            "_id": uuid.uuid4().hex,
            "username": username,
            "password": password,
            "encodings": ""
        }

        # Encrypt the password
        self.user['password'] = pbkdf2_sha256.encrypt(self.user['password'])

        # Check for existing email address
        if db.users.find_one({"username": self.user['username']}):
            return {"message": "username already in use", "code": 400}

        if db.users.insert_one(self.user):
            self.user = db.users.find_one({
                "username": username
            })
            
            print(self.user)
            
            return {"message": "success", "code": 200}

        return {"message": "Signup failed for unknown reason", "code": 400}

    async def signout(self):
        return {"message": "success", "code": 200}

    async def check_password(self, password):
        return self.user and pbkdf2_sha256.verify(password, self.user['password'])

    async def check_face_encodings(self, img):
        known_encodings = self.user['encodings']
        
        unknown_face_locations = face_recognition.face_locations(img)
        unknown_encodings = face_recognition.face_encodings(img, unknown_face_locations)

        status = 'ongoing'
        for known_encoding in known_encodings.split(';'):
            if True in face_recognition.compare_faces(unknown_encodings, known_encoding.decode('utf-8')):
                status = 'success'
                break

        return status
    
    async def update_face_encodings(self, img):       
        if self.user:
            face_locations = face_recognition.face_locations(img)
            if len(face_locations) != 1:
                return {"message": "ongoing", "code": 200}
            
            encoding = face_recognition.face_encodings(img, face_locations)[0]
            
            encoding_bytes = encoding.tobytes()
            
            if self.user['encodings'] == "":
                self.user['encodings'] = encoding_bytes.decode('utf-8')
            else:
                self.user['encodings'] += ";" + encoding_bytes.decode('utf-8')
                
            res = db.users.update_one(
                {'username': self.user['username']},
                {'$set': {'encodings': self.user['encodings']}}
            )
            
            print(res)
            
            num_encodings_saved = len(self.user['encodings'].split(';'))
            if num_encodings_saved >= MAX_NUM_ENCODINGS_SAVED:
                status = 'complete'
            else:
                status = 'ongoing'
            
            return {"message": status, "num_saved": num_encodings_saved, "code": 200}
            
        return {"message": "failure", "num_saved": len(self.user['encodings'].split(';')), "code": 400}
        
