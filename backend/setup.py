from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor
from logger import logger, logging
from langfuse import get_client
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pinecone import Pinecone
from constants import *
import nest_asyncio
from seed_data import seed_database
from pymongo import AsyncMongoClient
from db_models import *
from beanie import init_beanie
import time
import redis
import os

from utility import retry_thing, get_fresh_gcp_token

load_dotenv()

BASE_URL = os.getenv("BASE_URL") or ''
API_KEY = 'place-holder-key'
VDB_KEY = os.getenv("VDB_KEY") or ""
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY") or ""
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY") or ""
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL") or ""
REDIS_URL = os.getenv("REDIS_URL") or ""
MONGO_URI = os.getenv("MONGO_URI") or ""
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME") or ""
# In-memory cache variables
_CACHED_TOKEN: str | None = API_KEY
_TOKEN_EXPIRY_TIME: float = 0.0  # Epoch timestamp of when it dies

# --- Model

class DynamicVertexOpenAI(AsyncOpenAI):
    @property
    def api_key(self) -> str:
        """
        Whenever an agent uses this client, AsyncOpenAI checks self.api_key.
        This interceptor dynamically fetches a live token string right at that millisecond!
        """
        global _CACHED_TOKEN, _TOKEN_EXPIRY_TIME
    
        current_time = time.time()
        
        # If token doesn't exist, or has less than 5 minutes (300s) left, refresh it
        if _CACHED_TOKEN is None or (_TOKEN_EXPIRY_TIME - current_time) < 300:
            print("🎫 Cache miss or token expiring soon. Fetching fresh GCP token...")
            _CACHED_TOKEN = get_fresh_gcp_token()
            # Set expiry to 1 hour from now (minus a buffer to be safe)
            _TOKEN_EXPIRY_TIME = current_time + 3600 
        else:
            print("⚡ Cache hit! Serving token instantly from memory (0ms overhead).")
            
        return _CACHED_TOKEN

    @api_key.setter
    def api_key(self, value : str): # type: ignore[override]
        pass

if not BASE_URL or not API_KEY or not MODEL_NAME:
    logger.log(level=logging.ERROR, msg="BASE_URL, API_KEY, MODEL_NAME must be set via env var or code.")
    raise ValueError(
        "Please set BASE_URL, API_KEY, MODEL_NAME via env var or code."
    )
    
client = retry_thing(lambda:DynamicVertexOpenAI(base_url=BASE_URL, api_key=API_KEY))()

# --- Long Term Memory ( MongoDB )

async def init_db():
    logger.log(level=logging.INFO, msg="trying to connect Mongodb for long term memory")
    try: 
        mongo_client = AsyncMongoClient(MONGO_URI)
        
        # Provide the list of your collection classes to initialize indexes and links
        await init_beanie(
            database=mongo_client[MONGO_DB_NAME],
            document_models=[
                Order, 
                Customer,
            ]
        )
        await seed_database()
        logger.log(level=logging.INFO, msg="connected to Mongodb for long term memory")
    except Exception as e:
        logger.log(level=logging.ERROR, msg=f"failed to connect to Mongodb for long term memory, error: {e}")

# --- Short Term State ( Redis )
logger.log(level=logging.INFO, msg="trying to connect redis for short term state")
try:

    redis_client = redis.Redis.from_url(
        url=REDIS_URL,
        decode_responses=True
    )
    logger.log(level=logging.INFO, msg="connected to redis for short term state")
except Exception as e:
    logger.log(level=logging.ERROR, msg=f"failed to connect to redis for short term state, error: {e}")

# --- Seed Data in MongoDB

# try:
#     asyncio.run(seed_database())
# except Exception as e:
#     logger.log(level=logging.ERROR, msg=f"failed to seed data in MongoDB, error: {e}")

# --- Pinecone setup (Vector DB)

pc = retry_thing(lambda : Pinecone(api_key=VDB_KEY))()

# --- Langfuse setup
@retry_thing
def setup_langfuse():
    nest_asyncio.apply()
    OpenAIAgentsInstrumentor().instrument()
    return get_client()
 
langfuse = setup_langfuse()
# Verify connection
if langfuse.auth_check():
    logger.log(level=logging.INFO, msg="Langfuse client is authenticated and ready!")
else:
    logger.log(level=logging.ERROR, msg="Authentication failed. Please check your credentials and host.")


