#!/bin/sh

docker build -t tuttlsj1/cs4287:stream2fa -f ./services/app/Dockerfile ./services/app

sudo cat $TOKEN_PATH | docker login -u tuttlsj1 --password-stdin
docker push tuttlsj1/cs4287:stream2fa
docker logout
