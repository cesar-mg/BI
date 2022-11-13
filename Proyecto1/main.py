from typing import Optional

from fastapi import FastAPI, Body, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from joblib import dump, load
import os
from fastapi import FastAPI, HTTPException
app = FastAPI()

template = Jinja2Templates(directory="html")
app.mount("/static", StaticFiles(directory="html/static"), name = "static")
@app.get("/")
def read_root(request: Request):
   return template.TemplateResponse("index.html",{"request":request})

@app.post("/submit")
def handle_form(request:Request, cajita: str = Form(...)):
   model = load("html/static/assets/modelo.joblib")
   print(cajita)
   #result = model.predict(cajita)
   return template.TemplateResponse("index.html",{"request":request})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}
