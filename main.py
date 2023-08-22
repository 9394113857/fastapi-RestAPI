from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# CORS Configuration
origins = ["*"]  # Update this with the allowed origins
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# MySQL Configuration
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='raghu',
    database='nodejs_db'
)
mysql_cursor = mysql_conn.cursor(dictionary=True)

# MySQL Routes

@app.get('/mobiles')
def get_mobiles_mysql():
    mysql_cursor.execute('SELECT * FROM mobiles')
    mobiles = mysql_cursor.fetchall()
    return mobiles

@app.get('/mobiles/{id}')
def get_mobile_by_id_mysql(id: int):
    query = "SELECT * FROM mobiles WHERE id = %s"
    mysql_cursor.execute(query, (id,))
    mobile = mysql_cursor.fetchone()
    if mobile:
        return mobile
    else:
        raise HTTPException(status_code=404, detail="Mobile not found")

@app.post('/mobiles')
def add_mobile_mysql(data: dict):
    query = "INSERT INTO mobiles (name, price, ram, storage) VALUES (%s, %s, %s, %s)"
    values = (data['name'], data['price'], data['ram'], data['storage'])
    mysql_cursor.execute(query, values)
    mysql_conn.commit()
    return {"message": "Mobile added successfully"}

@app.put('/mobiles/{id}')
def update_mobile_mysql(id: int, data: dict):
    query = "UPDATE mobiles SET name = %s, price = %s, ram = %s, storage = %s WHERE id = %s"
    values = (data['name'], data['price'], data['ram'], data['storage'], id)
    mysql_cursor.execute(query, values)
    mysql_conn.commit()
    return {"message": "Mobile updated successfully"}

@app.delete('/mobiles/{id}')
def delete_mobile_mysql(id: int):
    query = "DELETE FROM mobiles WHERE id = %s"
    mysql_cursor.execute(query, (id,))
    mysql_conn.commit()
    return {"message": "Mobile deleted successfully"}

if __name__ == '__main__':
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=5000)  # You can change the host and port here
    uvicorn.run(app, port=5000)

    # uvicorn main:app --host 0.0.0.0 --port ${PORT:-5000}
    # This command uses the ${PORT:-5000} syntax, 
    # which means it will use the value of the PORT environment variable if it's set, 
    # otherwise it will default to 5000.
