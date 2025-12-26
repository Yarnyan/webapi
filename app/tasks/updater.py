import asyncio
from datetime import datetime
from sqlalchemy import select
from app.db.session import async_session
from app.models.weather import Weather
from app.services.weather import fetch_weather
from app.nats.pubsub import publish
from app.ws.manager import ws_manager

async def update_once():
    data = await fetch_weather()
    async with async_session() as session:
        w = Weather(**data)
        session.add(w)
        await session.commit()
        await session.refresh(w)

    await ws_manager.broadcast({"event": "weather_updated", "data": data})

    await publish("weather.updates", data)

async def periodic_updater(interval: int):
    while True:
        try:
            await update_once()
        except Exception as exc:
            print("[-] background update failed:", exc)
        await asyncio.sleep(interval)