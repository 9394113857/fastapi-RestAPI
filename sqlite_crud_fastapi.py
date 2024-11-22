from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3  # Import sqlite3 for SQLite database operations
import os  # Import os module for environment variable management

app = FastAPI()

# CORS Configuration
# This allows requests from any origin. Update `origins` to restrict access to specific origins.
origins = ["*"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

# SQLite Database Configuration
# SQLite database file is stored locally. Change 'sqlite_db.db' to your preferred database file name.
DB_PATH = "sqlite_db.db"

# Utility function to connect to the database
def get_db_connection():
    # Creates a connection to the SQLite database. If the file doesn't exist, it will be created.
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    return conn

# SQLite Routes

@app.get('/mobiles')
def get_mobiles_sqlite():
    """
    Retrieve all mobiles from the SQLite database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mobiles')
    mobiles = cursor.fetchall()
    conn.close()  # Close the connection after fetching data
    return [dict(mobile) for mobile in mobiles]  # Convert Row objects to dictionaries

@app.get('/mobiles/{id}')
def get_mobile_by_id_sqlite(id: int):
    """
    Retrieve a single mobile by its ID from the SQLite database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query, (id,))
    mobile = cursor.fetchone()
    conn.close()
    if mobile:
        return dict(mobile)
    else:
        raise HTTPException(status_code=404, detail="Mobile not found")

@app.post('/mobiles')
def add_mobile_sqlite(data: dict):
    """
    Add a new mobile to the SQLite database. Expects a JSON payload with 'name', 'price', 'ram', and 'storage'.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO mobiles (name, price, ram, storage) VALUES (?, ?, ?, ?)"
    values = (data['name'], data['price'], data['ram'], data['storage'])
    cursor.execute(query, values)
    conn.commit()  # Save changes to the database
    conn.close()
    return {"message": "Mobile added successfully"}

@app.put('/mobiles/{id}')
def update_mobile_sqlite(id: int, data: dict):
    """
    Update an existing mobile in the SQLite database by its ID. Expects a JSON payload with updated 'name', 'price', 'ram', and 'storage'.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE mobiles SET name = ?, price = ?, ram = ?, storage = ? WHERE id = ?"
    values = (data['name'], data['price'], data['ram'], data['storage'], id)
    cursor.execute(query, values)
    conn.commit()  # Save changes to the database
    conn.close()
    return {"message": "Mobile updated successfully"}

@app.delete('/mobiles/{id}')
def delete_mobile_sqlite(id: int):
    """
    Delete a mobile from the SQLite database by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM mobiles WHERE id = ?"
    cursor.execute(query, (id,))
    conn.commit()  # Save changes to the database
    conn.close()
    return {"message": "Mobile deleted successfully"}

if __name__ == '__main__':
    import uvicorn

    # Get the port from the environment variable or use the default (5000)
    port = int(os.environ.get("PORT", 5000))

    # Ensure the database and table exist before starting the app
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

    # Run the app with the specified port
    uvicorn.run(app, port=port)

# Instructions for running:
# 1. Save this script as `main.py`.
# 2. Run the script using `python main.py`.
# 3. The API will be available at http://localhost:5000 by default.

# Notes:
# - You can use environment variables to configure the database or port dynamically.
# - Test the API endpoints using tools like Postman, Curl, or a web browser.
# - Ensure SQLite is installed and accessible in your Python environment.

# SQLite is file-based, making it lightweight and easy to set up. This script includes basic CRUD operations and assumes a 'mobiles' table schema.
