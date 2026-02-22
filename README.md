# 🌤️ Sky by Riddhi

A full-stack weather application built with FastAPI (backend) and HTML/CSS/JavaScript (frontend). Users can search for weather by city or by using their current location, view a 5-day forecast, manage search history, and export stored data as CSV. This project was developed as part of the PM Accelerator Internship Program, demonstrating full-stack engineering, API integration, and database management skills.

------------------------------------------------------------------------

## Overview
<img width="1897" height="857" alt="image" src="https://github.com/user-attachments/assets/598e82ab-4268-45d0-8483-53d6c231cf7f" />
<img width="1897" height="787" alt="image" src="https://github.com/user-attachments/assets/680940cf-382d-4b63-8f83-3a9bb826e951" />


Sky by Riddhi is a modern weather application developed as part of the
**PM Accelerator Internship Project**. It demonstrates full-stack
development skills including API integration, database management,
RESTful architecture, and responsive frontend design.

------------------------------------------------------------------------

## Features

-   Search current weather by city name\
-   Detect weather using your current location (geolocation)\
-   View a 5-day forecast with icons and temperatures\
-   Receive travel advice based on weather conditions\
-   Store search history in a local SQLite database\
-   Edit and delete history records\
-   Export search history as a CSV file

------------------------------------------------------------------------

## Project Structure

    weather-app/
    ├── backend/
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── weather_service.py
    │   ├── routes/
    │   │   └── weather.py
    │   └── .env
    └── frontend/
        ├── index.html
        ├── script.js
        └── style.css

------------------------------------------------------------------------

## Prerequisites

-   Python 3.9 or higher\
-   pip\
-   A free OpenWeatherMap API key

------------------------------------------------------------------------

## Getting Started

### 1. Clone the repository

    git clone https://github.com/Riddhi2223/Sky-by-Riddhi.git
    cd Sky-by-Riddhi

### 2. Set up the backend

    cd backend
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # macOS/Linux
    pip install fastapi uvicorn sqlalchemy python-dotenv requests pandas

### 3. Configure your API key

Create a `.env` file inside the `backend/` folder:

    OPENWEATHER_API_KEY=your_api_key_here

Never commit your `.env` file.

### 4. Run the backend server

    uvicorn main:app --reload

API runs at: http://127.0.0.1:8000

Docs available at: http://127.0.0.1:8000/docs

### 5. Open the frontend

Open `frontend/index.html` in your browser.

Make sure the backend server is running.

------------------------------------------------------------------------

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/weather/?city={city}` | Get current weather by city |
| POST | `/weather/?lat={lat}&lon={lon}` | Get weather by coordinates |
| GET | `/weather/forecast?city={city}` | Get 5-day forecast |
| GET | `/weather/history` | Get last 10 searches |
| PUT | `/weather/history/{id}?new_city={city}` | Update a record |
| DELETE | `/weather/history/{id}` | Delete a record |
| GET | `/weather/export/csv` | Export history as CSV |

------------------------------------------------------------------------

## Technology Stack

Backend: FastAPI, Python\
Database: SQLite, SQLAlchemy\
Frontend: HTML, CSS, JavaScript\
Weather API: OpenWeatherMap\
Data Export: Pandas


