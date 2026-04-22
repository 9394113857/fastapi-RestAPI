import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sqlite_db.db")