# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from pb import assess_pb2 as pb_dot_assess__pb2


class AssessServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Assess = channel.unary_unary(
                '/AssessService/Assess',
                request_serializer=pb_dot_assess__pb2.AssessRequest.SerializeToString,
                response_deserializer=pb_dot_assess__pb2.AssessResponse.FromString,
                )


class AssessServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Assess(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AssessServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Assess': grpc.unary_unary_rpc_method_handler(
                    servicer.Assess,
                    request_deserializer=pb_dot_assess__pb2.AssessRequest.FromString,
                    response_serializer=pb_dot_assess__pb2.AssessResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AssessService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AssessService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Assess(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AssessService/Assess',
            pb_dot_assess__pb2.AssessRequest.SerializeToString,
            pb_dot_assess__pb2.AssessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
