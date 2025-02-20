# seed_data.py
from database import SessionLocal
from models import Supplier, ComplianceRecord
import pandas as pd
from datetime import datetime
import os
import ast

# Load data from Excel files
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
suppliers_df = pd.read_excel(os.path.join(data_dir, 'Task_Supplier_Data.xlsx'))
compliance_df = pd.read_excel(os.path.join(data_dir, 'Task_Compliance_Records.xlsx'))

db = SessionLocal()

# Seed suppliers
for index, row in suppliers_df.iterrows():
    supplier = Supplier(
        supplier_id=int(row['supplier_id']),
        name=row['name'],
        country=row['country'],
        compliance_score=int(row['compliance_score']),
        contract_terms=ast.literal_eval(row['contract_terms']),
        last_audit=pd.to_datetime(row['last_audit']).date()
    )
    db.add(supplier)

db.commit()

# Seed compliance records
for index, row in compliance_df.iterrows():
    record = ComplianceRecord(
        supplier_id=int(row['supplier_id']),
        metric=row['metric'],
        date_recorded=pd.to_datetime(row['date_recorded']).date(),
        result=row['result'],
        status=row['status']
    )
    db.add(record)

db.commit()
db.close()
