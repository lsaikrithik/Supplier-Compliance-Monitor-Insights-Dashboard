# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv  # Import dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Debugging Step: Print DATABASE_URL to check if it's loaded
if DATABASE_URL is None:
    raise ValueError("❌ DATABASE_URL is not set. Check your .env file or environment variables.")

print(f"✅ Using DATABASE_URL: {DATABASE_URL}")  # Debugging line

# ✅ Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
