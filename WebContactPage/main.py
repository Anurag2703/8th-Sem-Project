from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Allow CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create SQLite DB and table
conn = sqlite3.connect("contact_form.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

# Pydantic model for the form
class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/submit")
async def submit_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    conn = sqlite3.connect("contact_form.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()
    return {"message": "Form submitted successfully!"}

@app.get("/all_contacts")
async def get_contacts():
    conn = sqlite3.connect("contact_form.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows
