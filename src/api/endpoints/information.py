import sqlite3
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_information(char_name: str):
    conn = sqlite3.connect("inkin.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paragraphs WHERE character=?", (char_name,))
    result = cursor.fetchone()
    return {
        "charName": result[0],
        "basicDom": result[1],
        "meaningDom": result[2]
    }
