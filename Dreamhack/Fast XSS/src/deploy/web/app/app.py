from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request, data: str = '{"context": {"user": "Guest"}}'):
    try:
        data = json.loads(data)
    except:
        data = {"context": {"user": "Guest"}}
    context = {"name": "index.html", "request": request}|data
    return templates.TemplateResponse(**context)