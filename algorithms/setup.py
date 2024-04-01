import uvicorn
import base64

from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.score import gnn_score
from src.recognize import recog_cn_char
from src.comment import gpt_comment

app = FastAPI()


class EvaluateRequest(BaseModel):
    image_base64: str


@app.post("/evaluate")
async def evaluate_image(request: EvaluateRequest) -> Dict:
    try:
        score = gnn_score(request.image_base64)
        print(request.image_base64)
        file_bytes = base64.b64decode(request.image_base64)
        file_base64 = base64.b64encode(file_bytes).decode('utf-8')

        char_name = recog_cn_char(file_base64)
        # char_name, basic_dom, meaning_dom = get_char_and_infodom(file_base64)

        comment = gpt_comment(file_base64, char_name, score)
        print(comment)

        return {
            "score": score,
            "comment": comment,
            "charName": char_name
        }

    except Exception as e:
        # 记录错误日志
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/get_info")
async def evaluate_with_info(char: str):
    try:
        print(char)
        char_name, basic_dom, meaning_dom = get_cn_char_info(char)
        return {
            "charName": char_name,
            "basicDom": basic_dom,
            "meaningDom": meaning_dom
        }

    except Exception as e:
        # 记录错误日志
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=50051)
