from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import WeatherRequest
from weather_service import get_current_weather
from weather_service import get_five_day_forecast
from datetime import datetime
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/weather", tags=["Weather"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from datetime import datetime

@router.post("/")
def create_weather(
    city: str = None,
    lat: float = None,
    lon: float = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):

    # ------------------------
    # Date Validation
    # ------------------------
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            if start > end:
                raise HTTPException(
                    status_code=400,
                    detail="Start date must be before end date"
                )

        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD"
            )

    # ------------------------
    # Weather Fetch Logic
    # ------------------------
    try:
        if city:
            weather = get_current_weather(city=city)
        elif lat and lon:
            weather = get_current_weather(lat=lat, lon=lon)
            city = weather["location"]  # important for DB storage
        else:
            raise HTTPException(
                status_code=400,
                detail="City or coordinates required"
            )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ------------------------
    # Travel Advice
    # ------------------------
    def generate_travel_advice(temp, description):
        if temp > 30:
            return "Very hot! Stay hydrated and wear light clothes."
        elif temp < 5:
            return "Very cold! Wear heavy winter clothing."
        elif "rain" in description.lower():
            return "Rain expected. Carry an umbrella."
        elif "snow" in description.lower():
            return "Snow conditions. Travel carefully."
        else:
            return "Weather looks good for travel."

    advice = generate_travel_advice(
        weather["temperature"],
        weather["description"]
    )

    # ------------------------
    # Store in DB
    # ------------------------
    record = WeatherRequest(
        location=city,
        temperature=weather["temperature"],
        description=weather["description"]
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "location": record.location,
        "temperature": record.temperature,
        "description": record.description,
        "icon": weather["icon"],
        "travel_advice": advice
    }

@router.get("/")
def read_weather(db: Session = Depends(get_db)):
    return db.query(WeatherRequest).all()

@router.put("/{weather_id}")
def update_weather(weather_id: int, city: str, db: Session = Depends(get_db)):

    record = db.query(WeatherRequest).filter(WeatherRequest.id == weather_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    weather = get_current_weather(city)

    if not weather:
        raise HTTPException(status_code=404, detail="City not found")

    record.location = city
    record.temperature = weather["temperature"]
    record.description = weather["description"]

    db.commit()
    return record

@router.delete("/{weather_id}")
def delete_weather(weather_id: int, db: Session = Depends(get_db)):

    record = db.query(WeatherRequest).filter(WeatherRequest.id == weather_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Deleted successfully"}

import pandas as pd
from fastapi.responses import StreamingResponse
import io

@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):

    records = db.query(WeatherRequest).all()

    data = [
        {
            "location": r.location,
            "temperature": r.temperature,
            "description": r.description
        }
        for r in records
    ]

    df = pd.DataFrame(data)

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=weather.csv"}
    )

@router.get("/forecast")
def forecast(city: str):
    try:
        return get_five_day_forecast(city)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = (
        db.query(WeatherRequest)
        .order_by(WeatherRequest.id.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "city": record.location,
            "id": record.id,
            "temperature": record.temperature,
            "description": record.description
        }
        for record in records
    ]

@router.delete("/history/{record_id}")
def delete_weather(record_id: int, db: Session = Depends(get_db)):
    record = db.query(WeatherRequest).filter(WeatherRequest.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}

@router.put("/history/{record_id}")
def update_weather(record_id: int, new_city: str, db: Session = Depends(get_db)):
    record = db.query(WeatherRequest).filter(WeatherRequest.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Fetch updated weather
    weather = get_current_weather(new_city)

    record.location = new_city
    record.temperature = weather["temperature"]
    record.description = weather["description"]
    record.date_requested = datetime.utcnow()

    db.commit()
    db.refresh(record)

    return {"message": "Record updated successfully"}

@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    records = db.query(WeatherRequest).all()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["ID", "City", "Temperature", "Description", "Date Requested"])

    for record in records:
        writer.writerow([
            record.id,
            record.location,
            record.temperature,
            record.description,
            record.date_requested
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=weather_history.csv"}
    )