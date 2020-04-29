#! /usr/bin/env python3

from concurrent import futures
import grpc
import logging
import sys
import time

import cli_plugin_pb2
import cli_plugin_pb2_grpc

from grpc_health.v1.health import HealthServicer
from grpc_health.v1 import health_pb2, health_pb2_grpc

go_plugin_version = 1
app_protocol_version = 1
plugin_host = "0.0.0.0"
plugin_port = '50052'


class mine(cli_plugin_pb2_grpc.CLIServicer):
    """Provides methods that implement functionality of CLI plugin server."""

    def __init__(self):
        sys.stdout.flush()

        self.supported_commands = [
            cli_plugin_pb2.CommandDefinition(
                Use="hello",
                Short="hello",
                Long="hellooooo"
            )
        ]

    def Discover(self, request, context):
        return cli_plugin_pb2.DiscoverResponse(Commands=self.supported_commands)

    def Exec(self, request, context):
        for x in range(1, 5):
            output = f"command: {request.command}\nargs: {request.args}\n"

            yield cli_plugin_pb2.ExecResponse(
                stdout=bytes(output, "utf-8"),
                stderr=bytes())

            time.sleep(1)


def serve():
    # We need to build a health service to work with go-plugin
    health = HealthServicer()
    health.set(
        "plugin", health_pb2.HealthCheckResponse.ServingStatus.Value('SERVING'))

    # Start the server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    health_pb2_grpc.add_HealthServicer_to_server(health, server)

    cli_plugin_pb2_grpc.add_CLIServicer_to_server(mine(), server)
    server.add_insecure_port(f'{plugin_host}:{plugin_port}')

    server.start()

    sys.stdout.write(
        f"{go_plugin_version}|{app_protocol_version}|tcp|{plugin_host}:{plugin_port}|grpc\n"
    )

    sys.stdout.flush()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    serve()
