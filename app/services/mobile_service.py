from sqlalchemy import text
from app.db.database import engine

def get_all_mobiles():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM mobiles"))
        return [dict(row._mapping) for row in result]

def add_mobile(data):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO mobiles (name, price, ram, storage)
            VALUES (:name, :price, :ram, :storage)
        """), data)
        conn.commit()