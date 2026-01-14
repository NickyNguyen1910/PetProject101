from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Connect to an existing database
conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_NAME"),
        user=os.getenv("POSTGRES_USER"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PASSWORD"),
        cursor_factory=RealDictCursor
    )


@app.get("/books")
async def read_books():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
    return {"books": books}