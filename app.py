import asyncio
from threading import Thread

from fastapi import FastAPI, APIRouter, BackgroundTasks
from dotenv import load_dotenv
load_dotenv()

from cache import Cache
from push_data import PushData
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cache API",
    version="0.1",
    description="A simple API to add data to a cache and push it to a database",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
cache = Cache()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/push_data")
async def push_data(data: PushData):
    cache.add(data)
    return {"message": "Data added to cache"}


@app.on_event('startup')
async def app_startup():
    async def runner():
        while True:
            print("Running cache update")
            await cache.update_and_cleanup()
            await asyncio.sleep(5)

    thread = Thread(target=asyncio.run, args=(runner(),))
    thread.start()

