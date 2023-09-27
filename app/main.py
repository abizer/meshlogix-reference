from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Create a connection to SQLite database
conn = sqlite3.connect("status_updates.db", check_same_thread=False)
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
    # validation
    cursor.execute("SELECT author, apartment FROM status_updates GROUP BY author, apartment")
    authors = {author:apt for author, apt in cursor.fetchall()}
    if status.author in authors:
        if status.apartment != authors[status.author]:
            return {"error": "Integrity constraint violated: authors can only live in one apartment"}

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
