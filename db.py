from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch from .env
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# SQLAlchemy DB URL
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Engine creation
engine = create_engine(DATABASE_URL)

# Test connection
try:
    with engine.connect() as conn:
        print("✅ Connected to the database.")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
