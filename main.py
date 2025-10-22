import os
import asyncio
from fastapi import FastAPI
from routes.rose_ai_router import rose_watcher

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start your MongoDB watcher in the background
    asyncio.create_task(rose_watcher())

@app.get("/")
async def home():
    return {"message": "R.O.S.E is running in the background!"}

if __name__ == "__main__":
    # Bind to Render's $PORT if exists, otherwise use 8000 locally
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
