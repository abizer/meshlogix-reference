import fastapi 
import sqlite3
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Create a connection to SQLite database
conn = sqlite3.connect("status_updates.db")
cursor = conn.cursor()

# Data model
class StatusUpdate(BaseModel):
    timestamp: str
    author: str
    apartment: int
    post: str

# Database creation
def create_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status_updates (
            timestamp TEXT,
            author TEXT,
            apartment INTEGER,
            post TEXT
        )
    """)
    conn.commit()

create_db()

# API Endpoints
@app.get("/status")
def get_status():
    cursor.execute("SELECT * FROM status_updates ORDER BY timestamp DESC")
    return cursor.fetchall()

@app.post("/status")
def post_status(status: StatusUpdate):
    cursor.execute("INSERT INTO status_updates VALUES (?,?,?,?)", (status.timestamp, status.author, status.apartment, status.post))
    conn.commit()
    return {"message": "Status update has been posted successfully"}

@app.get("/status/{author}")
def get_status_by_author(author: str):
    cursor.execute("SELECT * FROM status_updates WHERE author=? ORDER BY timestamp DESC", (author,))
    return cursor.fetchall()

@app.get("/status/apartment/{apartment}")
def get_status_by_apartment(apartment: int):
    cursor.execute("SELECT * FROM status_updates WHERE apartment=? ORDER BY timestamp DESC", (apartment,))
    return cursor.fetchall()

# Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
