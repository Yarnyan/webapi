import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router
from app.db.base import Base
from app.db.session import engine
from app.tasks.updater import periodic_updater
from app.config import settings
from app.nats.pubsub import connect as nats_connect, close as nats_close

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await nats_connect()
    asyncio.create_task(periodic_updater(settings.update_interval_sec))
    yield

    await nats_close()

app = FastAPI(title="Сервис погоды", lifespan=lifespan)
app.include_router(router)