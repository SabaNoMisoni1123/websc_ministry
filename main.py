import json

from fastapi import FastAPI

app = FastAPI()

url_dict = []
with open("./data/urlList.json") as f:
    url_dict = json.load(f)
    print(url_dict)
    print(list(url_dict.keys()))


@app.get("/")
async def get_root():
    return {"message": "Hello World"}


@app.get("/help")
async def get_help():
    return {"message": "Help"}


@app.get("/list")
async def get_list():
    return {"message": url_dict}
