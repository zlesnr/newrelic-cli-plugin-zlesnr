#! /usr/bin/env python3

from concurrent import futures
import grpc
import logging
import sys
import time

import cli_plugin_pb2
import cli_plugin_pb2_grpc

go_plugin_version = 1
app_protocol_version = 1
plugin_host = "[::]"
plugin_port = '50052'


class CLIServicer(cli_plugin_pb2_grpc.CLIServicer):
    """Provides methods that implement functionality of CLI plugin server."""
    def __init__(self):
        self.supported_commands = [
            cli_plugin_pb2.CommandDefinition(
                Use="hello",
                Short="hello",
                Long="hellooooo"
            )
        ]

    def Exec(self, request, context):
        while True:
            output = f"""
            command: {request.command}
            args: {request.args}\n
            """

            yield cli_plugin_pb2.ExecResponse(
                stdout=bytes(output, "utf-8"),
                stderr=bytes())

            time.sleep(1)

    def Discover(self, request, context):
        return cli_plugin_pb2.DiscoverResponse(Commands=self.supported_commands)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cli_plugin_pb2_grpc.add_CLIServicer_to_server(CLIServicer(), server)
    server.add_insecure_port(f'{plugin_host}:{plugin_port}')

    server.start()

    sys.stdout.write(
        f"{go_plugin_version}|{app_protocol_version}|tcp|{plugin_host}:{plugin_port}|grpc"
    )
    sys.stdout.flush()

    sys.stderr.write(
        f"server: {server}"
    )

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
