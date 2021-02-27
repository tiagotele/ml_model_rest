from fastapi import FastAPI
import numpy as np
import os
import pickle
from pydantic import BaseSettings


# Change work dir to be where the script is exectued ("app" folder).
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

tags_metadata = [
    {
        "name": "Model",
        "description": "Calling ML model.",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

knn = pickle.load(open('iris.mdl', 'rb'))

labels = {0 : 'Setosa',
              1 : 'Versicolor',
              2 : 'Virginica'}

@app.get("/predict/", 
tags=["model"],
summary="Predict a class of Iris",
description="Pass the four required parameters to ML Model using KNN to classify irs type",
response_description="Iris type: Setosa, Versicolor or Virginca",
responses={
        "200": {
            "description": "Model Predicted"
        },
        "400": {
            "description": "Bad Request. The parameters must be greater than zero and less than 10",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
)
async def read_item(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
    input_data = np.asarray([sepal_length, sepal_width, petal_length, petal_width])
    predicted = knn.predict(input_data.reshape(1, -1) )
    return {
            "Predicted Iris": labels[int(predicted)]
            }
