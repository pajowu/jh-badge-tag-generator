from fastapi import FastAPI
from fastapi.responses import RedirectResponse, PlainTextResponse
from data import load_bottle_types, generate_stl, TagConfig

from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
async def index():
    return RedirectResponse("/static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/bottle_types")
async def bottle_types():
    return load_bottle_types()


@app.post("/generate_tag", response_class=PlainTextResponse)
async def generate_tag(body: TagConfig):
    return generate_stl(body)
