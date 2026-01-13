from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Connect to an existing database
conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )

# Open a cursor to perform database operations
cursor = conn.cursor()

#creating an endpoint/path

@app.get("/books")
async def read_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return {"books": books}
cursor.close()
conn.close()