from contextlib import asynccontextmanager
from random import Random
from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn
from call_agent import agent_loop
from typing import Optional
from setup import init_db
from logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Connecting to databases via init_db()...")
        await init_db()
        logger.info("Databases connected successfully!")
    except Exception as e:
        logger.error(f"🚨 CRITICAL: init_db failed on startup, but forcing boot anyway: {e}")
    yield

app = FastAPI(lifespan=lifespan)
allow_origins = [
    "http://localhost:3000",  # Next.js local development
    "http://localhost:5173",  # Vite local development
]

# ☁️ Dynamically pull the production frontend URL if it exists in the environment
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allow_origins.append(frontend_url)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    session_key: Optional[str] = ""

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/query")
async def query(request: QueryRequest):
    logger.info(f"request params: query: {request.query}, session_key: {request.session_key}")
    result = await agent_loop(
        query=request.query,
        session_key=request.session_key
    )

    return responses.JSONResponse(content=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)