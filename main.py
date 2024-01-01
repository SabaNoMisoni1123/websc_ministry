import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.wslib as wslib

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url_dict = []
with open("./data/urlList.json") as f:
    url_dict = json.load(f)


@app.get("/")
async def get_root():
    return {"message": "Hello World"}


@app.get("/help")
async def get_help():
    return {"message": "Help"}


@app.get("/list")
async def get_list():
    return {"message": url_dict}


@app.get("/test")
async def get_test():
    return wslib.test()
