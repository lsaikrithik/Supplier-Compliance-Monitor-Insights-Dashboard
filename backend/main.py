# main.py
from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from models import Base, Supplier, ComplianceRecord
from database import engine, SessionLocal
from schemas import SupplierCreate, ComplianceData, WeatherImpactData
from fastapi.middleware.cors import CORSMiddleware
from utils import generate_insights  
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/suppliers")
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@app.post("/suppliers")
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@app.get("/suppliers/{supplier_id}")
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@app.post("/suppliers/check-compliance")
def check_compliance(data: ComplianceData, db: Session = Depends(get_db)):
    compliance_record = ComplianceRecord(
        supplier_id=data.supplier_id,
        metric=data.metric,
        date_recorded=data.date_recorded.date(),  # Use the provided date
        result=data.result,
        status=data.status
    )
    db.add(compliance_record)
    db.commit()

    return {"message": "Compliance data uploaded and recorded."}

@app.get("/suppliers/insights/{supplier_id}")
def get_insights(supplier_id: int = Path(..., description="The ID of the supplier"), db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    records = db.query(ComplianceRecord).filter(ComplianceRecord.supplier_id == supplier_id).all()

    insights = generate_insights(supplier, records)
    return {"insights": insights}


@app.post("/suppliers/check-weather-impact")
def check_weather_impact(data: WeatherImpactData, db: Session = Depends(get_db)):
    # Extract data from the request
    supplier_id = data.supplier_id
    latitude = data.latitude
    longitude = data.longitude
    delivery_date = data.delivery_date.date()  # Ensure it's a date object

    # Check if the delivery date is within the next 5 days
    current_date = datetime.now().date()
    max_date = current_date + timedelta(days=5)

    if delivery_date < current_date:
        raise HTTPException(status_code=400, detail="Delivery date must be today or in the future.")
    if delivery_date > max_date:
        raise HTTPException(status_code=400, detail="Delivery date must be within the next 5 days.")

    # Fetch forecast weather data
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenWeatherMap API key not configured.")

    # OpenWeatherMap API endpoint for 5 Day / 3 Hour Forecast
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to fetch weather data: {response.text}")

    weather_data = response.json()

    # Analyze weather conditions for adverse weather
    adverse_conditions = False
    conditions_found = []

    # Find the forecast data for the delivery date
    target_datetime_start = datetime.combine(delivery_date, datetime.min.time())
    target_datetime_end = datetime.combine(delivery_date, datetime.max.time())

    for entry in weather_data.get('list', []):
        forecast_time = datetime.fromtimestamp(entry['dt'])
        if target_datetime_start <= forecast_time <= target_datetime_end:
            weather_conditions = [w['main'] for w in entry.get('weather', [])]
            if any(cond in ['Rain', 'Snow', 'Thunderstorm', 'Drizzle', 'Extreme'] for cond in weather_conditions):
                adverse_conditions = True
                conditions_found.extend(weather_conditions)

    # Update compliance record if adverse weather is detected
    if adverse_conditions:
        # Find the compliance record for the supplier and date
        compliance_record = db.query(ComplianceRecord).filter(
            ComplianceRecord.supplier_id == supplier_id,
            ComplianceRecord.date_recorded == delivery_date,
            ComplianceRecord.metric == 'Delivery Time',
            ComplianceRecord.status != 'Compliant'  # Only update if not already compliant
        ).first()

        if compliance_record:
            compliance_record.status = 'Excused - Weather Delay'
            db.commit()
            return {
                "message": "Delivery delay excused due to adverse weather conditions.",
                "conditions": list(set(conditions_found)),
            }
        else:
            return {
                "message": "No non-compliant delivery record found for the given supplier and date."
            }
    else:
        return {
            "message": "No adverse weather conditions forecasted on the delivery date."
        }
