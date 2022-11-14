from typing import Optional
from fastapi import FastAPI, Body, Request, Form,UploadFile,File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
from joblib import dump, load
import os
from fastapi import FastAPI, HTTPException
from preprocessing import process
import shutil
app = FastAPI()

template = Jinja2Templates(directory="html")
app.mount("/static", StaticFiles(directory="html/static"), name = "static")

@app.get("/",response_class=HTMLResponse)
def read_root(request: Request):
   return template.TemplateResponse("index.html",{"request":request})

@app.post("/submit")
def handle_form(request:Request, cajita: str = Form(...)):
   model = load("html/static/assets/modelo.joblib")
   data = process(cajita)
   prediction = model.predict(data)
   msg = "POSITIVO - INICIE PROTOCOLO DE EMERGENCIA"
   if prediction[0] == 0:
      msg = "Negativo"
   
   return template.TemplateResponse("index.html",{"request":request,"msg":msg})

@app.post("/file_analisis")
async def handle_form(request:Request, file: UploadFile = File(...)):
   with open("file.csv","wb") as buffer:
      shutil.copyfileobj(file.file,buffer)
   df=pd.read_csv('file.csv', sep=',', encoding = 'utf-8')
   df["text"] = df["text"].apply(process)
   model = load("html/static/assets/modelo.joblib")
   prediction = model.predict(df["text"])
   df["Predicted"] = prediction
   df.to_csv('/Predictions/DatosProcesados3.csv',encoding='utf-8')
   return template.TemplateResponse("index2.html",{"request":request})

@app.get("/file_analisis")
def read_item(request: Request):
   return template.TemplateResponse("index2.html",{"request":request})