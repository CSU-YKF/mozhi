from asyncio import futures

import grpc
import numpy
from PIL import Image
# import yaml

import pb.assess_pb2 as pb
import pb.assess_pb2_grpc as rpc

from concurrent import futures
import logging

import grpc
from python.pb import assess_pb2
from python.pb import assess_pb2_grpc


class Assess(assess_pb2_grpc.AssessServiceServicer):
    def Assess(self, request, context):
        #这是图片
        print("request: ", request.img)
        return assess_pb2.AssessResponse(score=0.5, comment="test")
        # Image.open(request.img).show()

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    assess_pb2_grpc.add_AssessServiceServicer_to_server(Assess(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()