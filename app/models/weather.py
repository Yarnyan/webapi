from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from app.db.base import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)