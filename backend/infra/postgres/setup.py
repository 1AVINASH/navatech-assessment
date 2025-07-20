import os
from dotenv import load_dotenv
import databases

load_dotenv()

class DatabaseClient:
    _instance = None

    def __init__(self):
        self._db = None
        self._initialized = False

    async def initialize(self):
        if not self._initialized:
            DB_USER = os.getenv("DB_USER")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            HOST = os.getenv("HOST") or "localhost"
            PORT = os.getenv("PORT") or 5432
            DBNAME = os.getenv("DBNAME") or "postgres"

            DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DBNAME}"
            self._db = databases.Database(DATABASE_URL)
            await self._db.connect()
            self._initialized = True

    @property
    def db(self) -> databases.Database:
        return self._db

    async def disconnect(self):
        if self._db:
            await self._db.disconnect()

db_cli = DatabaseClient()