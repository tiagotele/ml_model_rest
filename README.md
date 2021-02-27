# Sample REST API with ML

This repo runs a ML model on REST api using FastAPI.
The model used the iris dataset and was trained with KNN algorithm, where n = 3.
Next sessions show details about how to build/run.

## How to Run
```
./pipeline.sh
```

## Building docker image
```
docker build -t tiagotele/my_ml_model:1.0 .
```

## Running docker image available on DockerHub.
```
#docker run  --name my_ml_app -p 8000:8000 -t tiagotele/my_ml_model:1.0
```

## Pushing to DockerHub
```
docker login 
docker push tiagotele/my_ml_model:1.0
```

## Docker image
Docker image are available at [DockerHub](https://hub.docker.com/repository/docker/tiagotele/my_ml_model).
