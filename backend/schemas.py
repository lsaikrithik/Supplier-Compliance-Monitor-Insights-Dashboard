# schemas.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class SupplierCreate(BaseModel):
    name: str
    country: str
    compliance_score: int
    contract_terms: dict
    last_audit: datetime

class Supplier(BaseModel):
    supplier_id: int
    name: str
    country: str
    compliance_score: int
    contract_terms: dict
    last_audit: date

    class Config:
        orm_mode = True


class ComplianceData(BaseModel):
    supplier_id: int
    metric: str
    result: str
    status: str
    date_recorded: datetime  
    
class WeatherImpactData(BaseModel):
    supplier_id: int
    latitude: float
    longitude: float
    delivery_date: datetime
