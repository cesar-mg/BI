from cgitb import reset
from telnetlib import WONT
from typing import Optional, List
from fastapi import FastAPI
import pandas as pd
from joblib import dump, load
from DataModel import DataModel
from DataModelPredict import DataModelPredict
import os
from fastapi import FastAPI, HTTPException
from sklearn.metrics import r2_score as r2
app = FastAPI()


@app.post("/predict")
def make_predictions(dataModel: DataModelPredict):
    df = pd.DataFrame(dataModel.dict(), columns=dataModel.dict().keys(), index=[0])
    df.columns = dataModel.columns()
    fix_data(df)
    model = load("assets/modelo.joblib")
    result = model.predict(df)
    return {"Prediction": result[0]}

@app.post("/coefficient")
def calculate_r2(dataModels: List[DataModel]):
   if len(dataModels) < 2:
      raise HTTPException(status_code=412,detail= "Para el calculo de R2 se requieren al menos 2 registros")
   rows = []
   for dm in dataModels:
      rows.append(dm.dict())
   df = pd.DataFrame(rows, columns=dataModels[0].dict().keys())
   df.columns = dataModels[0].columns()
   X = df.drop("admission_points", axis = 1)
   Y = df["admission_points"]
   fix_data(X)
   model = load("assets/modelo.joblib")
   y = model.predict(X)
   result = r2(y,Y)
   return {"R2":result}

def fix_data(df):
   df["GRE Score"] = df["GRE Score"].apply(depurar_gre_score)
   df["GRE Score"] = df["GRE Score"].astype("float64")
   df["University Rating"] = df["University Rating"].apply(depurar_university_rating)
   df["University Rating"] = df["University Rating"].astype("float64")
   df["Research"] = df["Research"].apply(depurar_research)
   df["Research"] = df["Research"].astype("float64")
   df["Serial No."] = df["Serial No."].apply(lambda x: depurar_generico(x,50000))
   df["Serial No."] = df["Serial No."].astype("float64")
   df["TOEFL Score"] = df["TOEFL Score"].apply(lambda x: depurar_generico(x,120))
   df["TOEFL Score"] = df["TOEFL Score"].astype("float64")
   df["SOP"] = df["SOP"].apply(lambda x: depurar_generico(x,5))
   df["SOP"] = df["SOP"].astype("float64")
   df["LOR "] = df["LOR "].apply(lambda x: depurar_generico(x,5))
   df["LOR "] = df["LOR "].astype("float64")
   df["CGPA"] = df["CGPA"].apply(lambda x: depurar_generico(x,10))
   df["CGPA"] = df["CGPA"].astype("float64")
   return df
def depurar_gre_score(registro):
  try:
    registro = str(registro)
    num = ''.join(char for char in registro if char.isdigit() or char == '.')
    num = abs(int(float(num)))
  except:
   raise HTTPException(status_code=412,detail= "El valor de GRE_SCORE cuenta con errores.")
  if num > 340:
      raise HTTPException(status_code=412,detail= "El valor de GRE_SCORE es mayor a lo previsto.")
  return num
def depurar_university_rating(registro):
  try:
    registro = str(registro)
    num = ''.join(char for char in registro if char.isdigit() or char == '.')
    num = abs(int(float(num)))
  except:
   raise HTTPException(status_code=412,detail= "El valor de University Rating cuenta con errores.")
  if num > 5:
      num = 5
  return num

def depurar_research(registro):
  try:
    registro = str(registro)
    num = ''.join(char for char in registro if char.isdigit() or char == '.')
    num = abs(int(float(num)))
  except:
   raise HTTPException(status_code=412,detail= "El valor de Research cuenta con errores.")
  if num > 1:
      num = 1
  return num

def depurar_generico(registro,maximo):
  try:
    registro = str(registro)
    num = ''.join(char for char in registro if char.isdigit() or char == '.')
    num = abs(int(float(num)))
  except:
   raise HTTPException(status_code=412,detail= "Se encuentran errores.")
  if num > maximo:
      num = 1
  return num