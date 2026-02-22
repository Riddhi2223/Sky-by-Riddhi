import requests
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("Loaded API Key:", API_KEY)
def travel_advice(temp):
    if temp < 5:
        return "Very cold. Pack heavy winter clothing."
    elif 5 <= temp <= 20:
        return "Mild weather. Light jacket recommended."
    else:
        return "Warm weather. Light clothing recommended."

def get_current_weather(city: str = None, lat: float = None, lon: float = None):

    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    elif lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    else:
        raise HTTPException(status_code=400, detail="City or coordinates required")

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=data.get("message"))

    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]
    location = data["name"]

    return {
        "location": location,
        "temperature": temperature,
        "description": description,
        "icon": icon,
        "travel_advice": travel_advice(temperature)
    }

def get_five_day_forecast(city: str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise Exception(data.get("message", "Forecast unavailable."))

    forecast_list = []

    # API returns data every 3 hours — we’ll take one per day
    for item in data["list"][::8]:
        forecast_list.append({
        "date": item["dt_txt"],
        "temperature": item["main"]["temp"],
        "description": item["weather"][0]["description"],
        "icon": item["weather"][0]["icon"]
        })

    return forecast_list