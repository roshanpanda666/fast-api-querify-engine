from fastapi import FastAPI
import asyncio
from routes.rose_ai_router import rose_watcher  # your watcher function

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start the MongoDB watcher automatically on server start
    asyncio.create_task(rose_watcher())

@app.get("/")
async def home():
    return {"message": "R.O.S.E is running in the background!"}
