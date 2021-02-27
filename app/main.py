from fastapi import FastAPI
import numpy as np

import pickle

app = FastAPI()

knn = pickle.load(open('iris.mdl', 'rb'))

labels = {0 : 'Setosa',
              1 : 'Versicolor',
              2 : 'Virginica'}

@app.get("/predict/")
async def read_item(sepal_length: float = 0.0, sepal_width: float = 0.0, petal_length: float = 0.0, petal_width: float = 0.0):
    input_data = np.asarray([sepal_length, sepal_width, petal_length, petal_width])
    predicted = knn.predict(input_data.reshape(1, -1) )
    return {
            "Predicted Iris": labels[int(predicted)]
            }


@app.get("/")
async def root():
    return {"message": "Try the predict with something like this: http://localhost:8000/predict/?sepal_length=3.3&sepal_width=5&petal_length=0.8&petal_width=60.9 "}
