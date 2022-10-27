from cgitb import reset
from telnetlib import WONT
from typing import Optional, List
from fastapi import FastAPI
import pandas as pd
from joblib import dump, load
from DataModel import DataModel
from DataModelPredict import DataModelPredict
import os
from sklearn.metrics import r2_score as r2
app = FastAPI()


@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}

@app.post("/predict")
def make_predictions(dataModel: DataModelPredict):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    print("YA CASI")
    model = load("assets/modelo.joblib")
    print("AYDUA")
    result = model.predict(df)
    print(result)
    return {"Prediction": result[0]}
    
@app.post("/coefficient")
def calculate_r2(dataModels: List[DataModel]):
   rows = []
   for dm in dataModels:
      rows.append(dm.dict())
   print("DSA")
   df = pd.DataFrame(rows)
   df.columns = dataModels[0].columns()
   print(df)
   print("AAA")
   X = df.drop("admission_points", axis = 1)
   print("CASII")
   Y = df["admission_points"]
   print("BOMBAA")
   model = load("assets/modelo.joblib")
   print("CERCAAA")
   print(Y)
   y = model.predict(X)
   result = r2(y,Y)
   return {"R2":result}
