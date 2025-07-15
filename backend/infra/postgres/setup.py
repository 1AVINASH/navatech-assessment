import os
from dotenv import load_dotenv

import databases
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("HOST") or "localhost"
PORT = os.getenv("PORT") or 5432
DBNAME = os.getenv("DBNAME") or "postgres"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DBNAME}"
db = databases.Database(DATABASE_URL)