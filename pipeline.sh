#!/bin/bash

DOCKER_IMAGE_VERSION=1.1

pip3.9 install -r app/requirements.txt

rm app/iris.mdl

python3.9 app/train_model.py

docker rm $(docker ps -a -q)

docker build -t tiagotele/my_ml_model:$DOCKER_IMAGE_VERSION .

docker push tiagotele/my_ml_model:$DOCKER_IMAGE_VERSION