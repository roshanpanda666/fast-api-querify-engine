from fastapi import FastAPI
import asyncio
from routes.rose_ai_router import rose_watcher  # your watcher function

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start the MongoDB watcher automatically on server start
    asyncio.create_task(rose_watcher())

import os
import asyncio
from fastapi import FastAPI
from routes.rose_ai_router import rose_watcher

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(rose_watcher())

@app.get("/")
async def home():
    return {"message": "R.O.S.E is running in the background!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

async def home():
    return {"message": "R.O.S.E is running in the background!"}
