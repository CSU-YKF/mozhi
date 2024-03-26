import io
import grpc
import numpy as np
import uvicorn

from PIL import Image
from concurrent import futures

from pb import assess_pb2 as pb
from pb import assess_pb2_grpc as rpc
from deepmodel.main import main as gnn_score
from comment import gpt_comment
from typing import Dict
from fastapi import FastAPI, UploadFile, File


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


@app.post("/evaluate")
async def evaluate_image(file: UploadFile = File(...)) -> Dict:
    score = gnn_score(file)
    comment = gpt_comment(file, "书法", score)

    # 以下是假数据, 请结合实际情况进行修改
    character_type = "汉字"
    character_info = "这是一个很好的汉字"

    return {"score": score, "comment": comment, "character_type": character_type, "character_info": character_info}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=50051)
