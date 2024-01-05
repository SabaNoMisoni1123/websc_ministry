import json
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append("src")
import wslib

app = FastAPI()
ws_machine = wslib.MinistrySiteDataGetter()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:4173",
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

site_dict = dict()
with open("./data/urlList.json") as f:
    site_dict = json.load(f)


@app.get("/")
async def get_root():
    return {"message": "Hello World"}


@app.get("/help")
async def get_help():
    return {"message": "Help"}


@app.get("/siteList")
async def get_site_list(detail: bool = None):
    if detail is True:
        return {"msg": "Site List (detail)", "data": site_dict}
    else:
        ret_dict = dict()
        for k in site_dict.keys():
            ret_dict[k] = {
                "name": site_dict[k]["name"],
                "url": site_dict[k]["url"],
            }
        return {"msg": "Site List", "data": ret_dict}


@app.get("/data/")
async def get_data(id: str = "noID"):
    if id == "noID":
        return {
            "msg": "Need ID",
            "id": "No ID Selected",
            "url": "",
        }
    elif id not in site_dict.keys():
        return {
            "msg": "Invalid ID",
            "id": id,
            "url": "",
        }
    else:
        return {
            "msg": "SUCCESS",
            "id": id,
            "url": site_dict[id]["url"],
            "data": ws_machine.get(site_dict[id]),
        }
