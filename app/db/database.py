from sqlalchemy import create_engine, text
from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS mobiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price FLOAT,
                ram TEXT,
                storage TEXT
            )
        """))
        conn.commit()