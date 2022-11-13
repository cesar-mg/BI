from typing import Optional

from fastapi import FastAPI, Body, Request
from fastapi.templating import Jinja2Templates
app = FastAPI()

template = Jinja2Templates(directory="html")
@app.get("/")
def read_root(request: Request):
   return template.TemplateResponse("index.html",{"request":request})
@app.post("/submit")
def read_root(request: Request):
   return template.TemplateResponse("index.html",{"request":request})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}
