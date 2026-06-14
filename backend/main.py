from contextlib import asynccontextmanager
from random import Random
from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from call_agent import agent_loop
from typing import Optional
from setup import init_db
from logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:5173",  # Vite dev server
        # Add your production frontend URL here
    ],
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
    # result = {
    #     "message" : 'hi',
    #     "refund" : "denied",
    #     "session_key" : str(Random().randint(10000, 30000))
    # }
    result = await agent_loop(
        query=request.query,
        session_key=request.session_key
    )

    return responses.JSONResponse(content=result)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)