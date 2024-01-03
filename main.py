import json
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append("src")
import wslib as wslib

app = FastAPI()
ws_machine = wslib.MinistrySiteDataGetter()

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

url_dict = dict()
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


@app.get("/data")
async def get_data(id: str = ""):
    if id not in url_dict.key():
        return {
            "msg": "Invalid ID",
            "id": id,
            "url": "",
        }
    else:
        return {
            "msg": "SUCCESS",
            "id": id,
            "url": url_dict[id]["url"],
        }
