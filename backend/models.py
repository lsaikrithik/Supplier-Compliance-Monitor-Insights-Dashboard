# models.py
from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Supplier(Base):
    __tablename__ = 'suppliers'

    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    country = Column(String)
    compliance_score = Column(Integer)
    contract_terms = Column(JSON)
    last_audit = Column(Date)

class ComplianceRecord(Base):
    __tablename__ = 'compliance_records'

    compliance_record_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'))
    metric = Column(String)
    date_recorded = Column(Date)
    result = Column(String)
    status = Column(String)


