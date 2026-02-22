from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class WeatherRequest(Base):
    __tablename__ = "weather_requests"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    temperature = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)