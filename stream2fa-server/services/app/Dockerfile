FROM animcogn/face_recognition:cpu

COPY requirements.txt /requirements.txt

RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . /app/

WORKDIR /app/

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0"]
