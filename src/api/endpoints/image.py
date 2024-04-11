import imghdr
import sqlite3
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException

from algorithms.src import evaluate_image

app = FastAPI()


def is_image(file: UploadFile):
    # 判断文件是否为图片类型
    file_type = imghdr.what(file.file)
    file.file.seek(0)  # 将文件指针重置到开头
    return file_type in ["jpeg", "png", "gif", "bmp"]


async def store_image(data_blob: bytes):
    conn = sqlite3.connect("inkin.db")

    # 将文件存储到SQLite数据库中
    cursor = conn.cursor()
    try:
        # 将文件存储到SQLite数据库中
        cursor.execute("INSERT INTO image (data) VALUES (?)", (data_blob,))
        conn.commit()  # 提交更改
        print("图片已成功存储到数据库中")
    except sqlite3.Error as e:
        print(f"将图片存储到数据库时出错: {e}")
    finally:
        conn.close()  # 关闭数据库连接


async def process_image(data_blob: bytes):
    data_base64 = base64.b64encode(data_blob).decode("utf-8")
    # 评估图像
    result = evaluate_image(data_base64)
    print(result)
    return result


def store_result(result_json: dict):
    conn = sqlite3.connect("inkin.db")

    # 将结果存储到SQLite数据库中
    cursor = conn.cursor()
    try:
        # 将结果存储到SQLite数据库中
        cursor.execute("INSERT INTO assess (score, comment, character_name) VALUES (?, ?, ?)",
                       (result_json["score"], result_json["comment"], result_json["charName"]))
        conn.commit()  # 提交更改
        print("结果已成功存储到数据库中")
    except sqlite3.Error as e:
        print(f"将结果存储到数据库时出错: {e}")
    finally:
        conn.close()  # 关闭数据库连接


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # 检查文件是否为图片类型
    if not is_image(file):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    # 处理上传的文件
    file_content = file.file.read()
    await store_image(file_content)
    await process_image(file_content)

    # return {"filename": file.filename, "content_type": file.content_type}


@app.get("/get_image/{image_id}")
async def get_image(image_id: int) -> bytes:
    """
    get image的ID（参数）
    """
    conn = sqlite3.connect("inkin.db")
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM image WHERE id=?", (image_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return result[0]


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
