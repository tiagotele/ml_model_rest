from fastapi import FastAPI, Query,HTTPException
import numpy as np
import os
import pickle
from pydantic import BaseSettings
from fastapi.openapi.utils import get_openapi

APP_VERSION="1.0.1"

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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Machine Learning REST Endpoint",
        version=APP_VERSION,
        description="API to consume ML service.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

knn = pickle.load(open('iris.mdl', 'rb'))

labels = {0: 'Setosa',
          1: 'Versicolor',
          2: 'Virginica'}


@app.get("/predict/",
         tags=["Model"],
         summary="Predict a class of Iris",
         description="Endpoint that return Iris type( Setosa, Versicolor or Virginca) when passed the botanical parts.",
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
                             "detail": "Bad Request. The parameters must be greater than zero and less than 10"
                         }
                     }
                 }
             },
             "422": {
                 "description": "Validation Error. Only numbers are allowed"
             }
         }
         )
async def read_item(
        sepal_length: float = Query(..., description="Size of sepal length in in centimeters"),
        sepal_width: float = Query(..., description="Size of sepal width in in centimeters"),
        petal_length: float = Query(..., description="Size of petal length in in centimeters"),
        petal_width: float = Query(..., description="Size of petal width in in centimeters")
) :
    input_data = np.asarray([sepal_length, sepal_width, petal_length, petal_width])

    for i in input_data:
        if float(i) <= 0.0 or float(i) > 10.0:
            raise HTTPException(status_code=400, detail="Bad Request")

    predicted = knn.predict(input_data.reshape(1, -1))
    return {
        "iris_type": labels[int(predicted)]
    }
