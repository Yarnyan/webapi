import json
from nats.aio.client import Client as NATS
from app.config import settings

nc = NATS()

async def connect():
    await nc.connect(settings.nats_url)

async def close():
    await nc.close()

async def publish(subject: str, data: dict):
    await nc.publish(subject, json.dumps(data).encode())

async def subscribe(subject: str, cb):
    async def wrapper(msg):
        data = json.loads(msg.data.decode())
        await cb(data)
    await nc.subscribe(subject, cb=wrapper)