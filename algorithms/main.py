import io
import grpc
import numpy as np
import uvicorn
import base64

from PIL import Image
from concurrent import futures

from pb import assess_pb2 as pb
from pb import assess_pb2_grpc as rpc
from deepmodel.main import main as gnn_score
from comment import gpt_comment
from typing import Dict
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from charinfo import *

# class Assess(rpc.AssessServiceServicer):
#     def Assess(self, request, context):
#         # print("request: ", request.img)
#         img_stream = io.BytesIO(request.img)
#         img = Image.open(img_stream)
#         img_np = np.array(img)
#         print(f"Load success, {img_np.shape}")
#         s = score(img) + 3
#         if s >= 10:
#             s = 9 + np.random.randn()
#         noise = np.random.normal(0, 3, 3)
#         f = np.array([s, s, s], dtype=np.float16)
#         f = f + noise
#         c = comments(float(f[0]), float(f[1]), float(f[2]))
#         return pb.AssessResponse(score=s, comment=c)
#         # Image.open(request.img).show()
#
#
# def serve():
#     port = "50051"
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     rpc.add_AssessServiceServicer_to_server(Assess(), server)
#     server.add_insecure_port("[::]:" + port)
#     server.start()
#     print("Server started, listening on " + port)
#     server.wait_for_termination()


app = FastAPI()


class EvaluateRequest(BaseModel):
    image_base64: str


@app.post("/evaluate")
async def evaluate_image(request: EvaluateRequest) -> Dict:
    try:
        # score = gnn_score(request.image_base64)
        print(request.image_base64)
        file_bytes = base64.b64decode(request.image_base64)
        # upload_file = UploadFile(filename="image.jpg", file=io.BytesIO(file_bytes))

        score = 6.0

        file_base64 = base64.b64encode(file_bytes).decode('utf-8')

        char_name = recog_cn_char(file_base64)
        # char_name, basic_dom, meaning_dom = get_char_and_infodom(file_base64)

        comment = gpt_comment(file_base64, char_name, score)
        print(comment)
        # 以下是假数据, 请结合实际情况进行修改
        # character_type = "汉字"
        # character_info = "这是一个很好的汉字"

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
