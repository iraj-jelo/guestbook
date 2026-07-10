import os
import logging
import sys

import redis
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    format="%(levelname)s:     %(message)s",
    # format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    # datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("fastapi_app")

logging.info(f"Get hosts from {os.getenv('GET_HOSTS_FROM', 'env')}")


def redis_leader():
    host = os.getenv(
        "REDIS_LEADER_SERVICE_HOST",
        "redis-leader"
    )

    return redis.Redis(
        host=host,
        port=6379,
        decode_responses=True
    )


def redis_follower():
    host = os.getenv(
        "REDIS_FOLLOWER_SERVICE_HOST",
        "redis-follower"
    )

    return redis.Redis(
        host=host,
        port=6379,
        decode_responses=True
    )


@app.get("/api/messages")
def get_messages():
    client = redis_follower()

    value = client.get("guestbook")

    if not value:
        return {"messages": []}

    return {
        "messages": value.split(",")
    }


@app.post("/api/messages")
def add_message(message: str):
    client = redis_leader()

    current = client.get("guestbook")

    messages = []

    if current:
        messages = current.split(",")

    messages.append(message)

    client.set(
        "guestbook",
        ",".join(messages)
    )

    return {"status": "updated"}


app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)
