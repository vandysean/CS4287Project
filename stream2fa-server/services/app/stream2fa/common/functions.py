import cv2
import numpy as np
import base64

async def decode_base64_image(uri):
   img_encoded_b64 = uri.split(',')[1]
   img_np_arr = np.frombuffer(base64.b64decode(img_encoded_b64), np.uint8)
   img = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)

   return img
