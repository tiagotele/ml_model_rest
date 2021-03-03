# Sample REST API with ML

This repo runs a ML model on REST api using FastAPI.
The model used the iris dataset and was trained with KNN algorithm, where n = 3.
Next sessions show details about how to build/run.

## Requirements
To successfully take advantage of this repo is required have a machine with
- Python 3.9 installed. If you have 3.x, make sure to change python version on  [`pipeline.sh`](pipeline.sh) .
- Install python dependencies available on [`requirements`](app/requirements.txt) file.
- Docker installed. Dockerhub account is desirable if you wish deploy docker image there.

## How to Run
```
./pipeline.sh
```

## Building docker image
```
docker build -t tiagotele/my_ml_model:1.1 .
```

## Running docker image available on DockerHub.
```
docker run  --name my_ml_app -p 8000:8000 -t tiagotele/my_ml_model:1.1
```

## Pushing to DockerHub
```
docker login 
docker push tiagotele/my_ml_model:1.1
```

## Docker image
Docker image are available at [DockerHub](https://hub.docker.com/repository/docker/tiagotele/my_ml_model).

## Swagger documentation
The Swagger documentation is available at /docs endpoint of this app. 
You can access after running a docker image on the address just access the [/doc endpoint](http://localhost:8000/docs).

## AWS Architecture

![AWS Architecture](docs/AWS_Architecture.jpeg)

The above image represents and initial AWS Architecture for this ML Rest service.

There are the main blocks on gray background. They have its own purpose.

### IaC Module
The infrastructure as a code module is in charge of build the whole infrastructure and AWS components. It can be done with Terraform or AWS Cloudformation.

### Data Module
Is a S3 Datalake. This data is periodically versioned(can be a folder inside the same bucket but with the most updated data) and treated as a single dataset.

### ML Pipeline Module
This modules is done by a EC2 Spot instance to save cost. A custom EC2 image will be build with needed packages/softwares to fetch data from S3, train a new ML model, build a new Docker image and deploy this image into a AWS Elastic Container Registry(ECR). After this new image is pushed to ECR, a AWS Lambda function will update a Dynamo table that has as key/value the S3 dataset version and ECR image version. 


### Observability Module
Some metrics and rules will be created to continuously monitor the REST API. In case of trouble it will call AWS SNS to notify operations team on Slack Channel.

### REST Api Serverless Module
This is a REST API build on AWS Serverless stack. The AWS Cloudfront will be on edge and delivery and API Gateway that send its data api calls to AWS Lambda. This Lambda will run a Docker image existing on ECR.

### Pros and Cons of the architecture

This architecture aims to be a low cost ML Data Pipeline. It has a general purpose and is a cost effective. For performance requirements and more robust ML Models, as using Neural Nets, using a SageMaker pipeline to automate training and deploy would be more properly. It may incurs bigger costs.
