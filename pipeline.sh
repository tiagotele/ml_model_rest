#!/bin/bash

pip3.9 install -r app/requirements.txt

rm app/iris.mdl

python3.9 app/train_model.py

docker rm $(docker ps -a -q)

docker build -t tiagotele/my_ml_model:1.0 .

docker push tiagotele/my_ml_model:1.0