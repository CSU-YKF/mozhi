import os
import sqlite3
import base64
import uuid
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi import File, UploadFile, HTTPException, FastAPI
from starlette.responses import Response

from src.services import evaluate_image

from src.recognize import get_cn_char_info

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:12345"],  # 允许的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    # 返回image的ID
    return cursor.lastrowid


async def process_image(image_upload_file: UploadFile):
    # 生成唯一的文件名
    file_extension = os.path.splitext(image_upload_file.filename)[1]
    unique_filename = str(uuid.uuid4()) + file_extension

    # 保存上传的文件到本地文件系统和数据库
    file_path = os.path.join("uploads", unique_filename)
    with open(file_path, "wb") as file:
        file.write(await image_upload_file.read())

    # 评估图像
    result = await evaluate_image(file_path)
    image_id = await store_image(open(file_path, "rb").read())

    # 将image的ID添加到评估结果中
    result["image_id"] = image_id

    return result


def store_result(result_json: dict):
    conn = sqlite3.connect("inkin.db")

    # 将结果存储到SQLite数据库中
    cursor = conn.cursor()
    try:
        # 将结果存储到SQLite数据库中
        cursor.execute("INSERT INTO assess (score, comment, character_name, image_id) VALUES (?, ?, ?, ?)",
                       (result_json["score"], result_json["comment"], result_json["charName"], result_json["image_id"]))
        conn.commit()  # 提交更改
        print("结果已成功存储到数据库中")
    except sqlite3.Error as e:
        print(f"将结果存储到数据库时出错: {e}")
    finally:
        conn.close()  # 关闭数据库连接


@app.post("/upload")
async def upload(image: UploadFile = File(...)):
    # 检查文件是否为图片类型
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    result = await process_image(image)
    # 插入assessment
    store_result(result)

    return {"信息": "图片上传成功"}


@app.get("/getAllAssessment")
async def get_all_assessment():
    """
    返回一个列表，包含所有评估结果，评价结果从DB的assess表中读取。
    """
    conn = sqlite3.connect("inkin.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assess")
    results = cursor.fetchall()
    print(results)
    return results


@app.get("/getImage/{image_id}")
async def get_image(image_id: int) -> Response:
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
    image_data = result[0]
    return Response(content=image_data, media_type="image")


@app.get("/getInformation/{char_name}")
async def get_information(char_name: str):
    conn = sqlite3.connect("inkin.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT character, basic_dom, meaning_dom FROM paragraphs WHERE character=?", (char_name,))
        result = cursor.fetchone()
        print("wocaonimam", result)

        if result is not None:
            return {
                "character": result[0],
                "basicDom": result[1],
                "meaningDom": result[2]
            }
        else:
            char_name, basic_dom, meaning_dom = get_cn_char_info(char_name)
            cursor.execute("INSERT INTO paragraphs (character, basic_dom, meaning_dom) VALUES (?, ?, ?)",
                           (char_name, basic_dom, meaning_dom))
            conn.commit()

            return {
                "character": char_name,
                "basicDom": basic_dom,
                "meaningDom": meaning_dom
            }
    except sqlite3.Error as e:
        print(f"数据库操作错误: {e}")
        raise HTTPException(status_code=500, detail="数据库操作错误")
    finally:
        conn.close()

@app.get("/getAllAssessment")
async def get_all_assessment():
    """
    返回一个列表，包含所有评估结果，评价结果从DB的assess表中读取。
    """
    conn = sqlite3.connect("inkin.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assess")
    results = cursor.fetchall()
    print(results)
    return results


uvicorn.run(app, host="0.0.0.0", port=8080)
