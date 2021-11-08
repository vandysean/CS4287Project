FROM animcogn/face_recognition:cpu

COPY . /app/

WORKDIR /app/

RUN python -m pip install --upgrade pip \
 && pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0"]
