from fastapi import FastAPI
from database import engine, Base
from routes import weather

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(weather.router)

@app.get("/")
def root():
    return {"message": "Weather API Running"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)