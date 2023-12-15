import io
import grpc
import numpy as np
from pb import assess_pb2 as pb
from pb import assess_pb2_grpc as rpc
from PIL import Image
from concurrent import futures

from deepmodel.main import main as score
from comment.ernie_comment import main as comments


class Assess(rpc.AssessServiceServicer):
    def Assess(self, request, context):
        # print("request: ", request.img)
        img_stream = io.BytesIO(request.img)
        img = Image.open(img_stream)
        img_np = np.array(img)
        print(f"Load success, {img_np.shape}")
        s = score(img)
        c = comments()
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
