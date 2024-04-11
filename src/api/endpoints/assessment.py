import sqlite3
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_all_assessment():
    """
    返回一个列表，包含所有评估结果，评价结果从DB的assess表中读取。
    """
    conn = sqlite3.connect("inkin.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assess")
    results = cursor.fetchall()
    return results
