import io
import grpc
import numpy as np

from PIL import Image
from concurrent import futures

from pb import assess_pb2 as pb
from pb import assess_pb2_grpc as rpc
from deepmodel.main import main as score
from comment.ernie_comment import main as comments


class Assess(rpc.AssessServiceServicer):
    def Assess(self, request, context):
        # print("request: ", request.img)
        img_stream = io.BytesIO(request.img)
        img = Image.open(img_stream)
        img_np = np.array(img)
        print(f"Load success, {img_np.shape}")
        s = score(img) + 3
        if s >= 10:
            s = 9 + np.random.randn()
        noise = np.random.normal(0, 3, 3)
        f = np.array([s, s, s], dtype=np.float16)
        f = f + noise
        c = comments(float(f[0]), float(f[1]), float(f[2]))
        return pb.AssessResponse(score=s, comment=c)
        # Image.open(request.img).show()


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_AssessServiceServicer_to_server(Assess(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
