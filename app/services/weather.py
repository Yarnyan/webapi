import httpx
from app.config import settings
from datetime import datetime

async def fetch_weather() -> dict:
    params = {
        "latitude": settings.lat,
        "longitude": settings.lon,
        "current_weather": "true",
        "hourly": "relativehumidity_2m",
        "timezone": "auto",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(settings.open_meteo_url, params=params)
        r.raise_for_status()
        data = r.json()

    current = data["current_weather"]
    humidity = data["hourly"]["relativehumidity_2m"][0]

    return {
        "temperature": current["temperature"],
        "humidity": humidity,
        "wind_speed": current["windspeed"],
    }