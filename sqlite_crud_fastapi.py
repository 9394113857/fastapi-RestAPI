from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

# ==============================
# CORS Configuration
# ==============================
# Allows requests from any origin.
# In production, replace "*" with your frontend URL.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==============================
# SQLite Database Configuration
# ==============================

DB_PATH = "sqlite_db.db"

def get_db_connection():
    """
    Create and return a SQLite database connection.
    If DB file does not exist, it will be created automatically.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==============================
# ROUTES
# ==============================

@app.get("/mobiles")
def get_mobiles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mobiles")
    mobiles = cursor.fetchall()
    conn.close()
    return [dict(mobile) for mobile in mobiles]


@app.get("/mobiles/{id}")
def get_mobile_by_id(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mobiles WHERE id = ?", (id,))
    mobile = cursor.fetchone()
    conn.close()

    if mobile:
        return dict(mobile)
    else:
        raise HTTPException(status_code=404, detail="Mobile not found")


@app.post("/mobiles")
def add_mobile(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO mobiles (name, price, ram, storage) VALUES (?, ?, ?, ?)",
        (data["name"], data["price"], data["ram"], data["storage"])
    )

    conn.commit()
    conn.close()

    return {"message": "Mobile added successfully"}


@app.put("/mobiles/{id}")
def update_mobile(id: int, data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE mobiles SET name = ?, price = ?, ram = ?, storage = ? WHERE id = ?",
        (data["name"], data["price"], data["ram"], data["storage"], id)
    )

    conn.commit()
    conn.close()

    return {"message": "Mobile updated successfully"}


@app.delete("/mobiles/{id}")
def delete_mobile(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mobiles WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"message": "Mobile deleted successfully"}


# ==============================
# MAIN ENTRY
# ==============================

if __name__ == "__main__":
    import uvicorn

    # Get PORT from environment variable (Render/Production)
    # If not available, default to 5000
    port = int(os.environ.get("PORT", 5000))

    # Ensure table exists before starting app
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mobiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            ram TEXT NOT NULL,
            storage TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    # Start FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=port)

# ✅ 🔥 Single Line Dynamic Run (Windows PowerShell)
# $env:PORT=5500; py sqlite_crud_fastapi.py

# 1️⃣ $env:PORT=5500

# Sets environment variable PORT

# Only for this terminal session

# Windows PowerShell syntax

# ✅ Single Line Remove + Run
# Remove-Item Env:PORT; py sqlite_crud_fastapi.py

# ✅ Run only:-
# py sqlite_crud_fastapi.py

# The default port for FastAPI (Uvicorn) is:
# 8000, but we have set it to 5000 in the code for consistency with Render's default port.

# The default port for FastAPI (Uvicorn) is:

# 8000

# If you run:

# uvicorn main:app --reload

# you'll see:

# Uvicorn running on http://127.0.0.1:8000

# and access:

# http://localhost:8000
# http://localhost:8000/docs

# In your code, however, you have:

# port = int(os.environ.get("PORT", 5000))

# So if no PORT environment variable is set, your app runs on:

# http://localhost:5000

