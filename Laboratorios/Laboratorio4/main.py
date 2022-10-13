from typing import Optional
from fastapi import FastAPI
import pandas as pd
from joblib import dump, load
from DataModel import DataModel
import os
app = FastAPI()


@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}

@app.post("/predict")
def make_predictions(dataModel: DataModel):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    print("YA CASI")
    model = load("assets/modelo.joblib")
    print("AYDUA")
    result = model.predict(df)
    print(result)
    return result
