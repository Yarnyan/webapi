from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from app.db.session import async_session
from app.models.weather import Weather
from app.tasks.updater import update_once
from app.ws.manager import ws_manager

router = APIRouter()

@router.get("/items")
async def list_weather(limit: int = 100):
    async with async_session() as session:
        stmt = select(Weather).order_by(Weather.created_at.desc()).limit(limit)
        rows = (await session.execute(stmt)).scalars().all()
        return rows

@router.get("/items/{item_id}")
async def get_weather(item_id: int):
    async with async_session() as session:
        return await session.get(Weather, item_id)

@router.post("/items")
async def create_weather(temperature: float, humidity: float, wind_speed: float):
    async with async_session() as session:
        w = Weather(temperature=temperature, humidity=humidity, wind_speed=wind_speed)
        session.add(w)
        await session.commit()
        await session.refresh(w)
        return w

@router.patch("/items/{item_id}")
async def patch_weather(item_id: int, temperature: float | None = None,
                        humidity: float | None = None, wind_speed: float | None = None):
    async with async_session() as session:
        w = await session.get(Weather, item_id)
        if temperature is not None:
            w.temperature = temperature
        if humidity is not None:
            w.humidity = humidity
        if wind_speed is not None:
            w.wind_speed = wind_speed
        await session.commit()
        return w

@router.delete("/items/{item_id}")
async def delete_weather(item_id: int):
    async with async_session() as session:
        w = await session.get(Weather, item_id)
        await session.delete(w)
        await session.commit()
        return {"ok": True}

@router.post("/tasks/run")
async def run_task():
    await update_once()
    return {"status": "Фоновая задача тригернута"}

@router.websocket("/ws/items")
async def websocket_endpoint(ws: WebSocket):
    await ws_manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)