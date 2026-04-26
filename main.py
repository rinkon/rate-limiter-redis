from fastapi import FastAPI, Request, Response, status
from contextlib import asynccontextmanager
from redis.asyncio import Redis
from time import time
import os

TOKEN_REFILL_RATE = int(os.getenv("TOKEN_REFILL_RATE"))
BUCKET_CAPACITY = int(os.getenv("BUCKET_CAPACITY"))
# required token varies for different resource consuming apis
REQUIRED_TOKEN = int(os.getenv("REQUIRED_TOKEN"))
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))


redis_client = None


async def get_script_hash():
    #reads from a file
    with open('token_bucket.lua', 'r') as f:
        script_content = f.read()
    #loads the content to redis using redis.load_script
    return await redis_client.script_load(script_content)
    
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    #instantiate redis client
    #load the token_bucket.lua script to redis and generate the hash
    #fills two global vars redis_client and script_hash

    global redis_client, script_hash
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT)
    script_hash = await get_script_hash()

    yield
    await redis_client.close()


app = FastAPI(lifespan=lifespan)

@app.middleware('http')
async def check_request(request: Request, call_next):
    # 1. asks for clients ip to create unique key
    # 2. creates unique keys for redis for checking how many tokens available, and last request timestamp
    # 3. sends these to redis, 2nd argument is length of KEYS in luascript, so here, after keys, all are ARGS
    # 4. if allowed: calls the destination of the request and sends response back
    # 5. else: 429, Too Many Requests

    # 1
    client_ip = request.client.host
    # 2
    token_count_key = client_ip + ".token_count"
    timestamp_key = client_ip + ".timestamp"
    # 3
    allowed, remaining_token_count = await redis_client.evalsha(script_hash, 2, token_count_key, timestamp_key, TOKEN_REFILL_RATE, BUCKET_CAPACITY, time(), REQUIRED_TOKEN)

    if allowed:
        # 4
        response = await call_next(request)
        response.headers["X-Remaining-Tokens"] = str(remaining_token_count)
        return response
    else:
        # 5
        return Response(
            content= "Too Many Requests",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            media_type="text/plain",
            headers={"X-Remaining-Tokens": "0"}
        )
    


@app.get('/hello')
def endpoint():
    return {"message": "This is a rate limited endpoint"}
