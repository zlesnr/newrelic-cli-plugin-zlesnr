#! /usr/bin/env python3

from __future__ import print_function

import random
import logging

import grpc

import cli_plugin_pb2
import cli_plugin_pb2_grpc

plugin_host = "0.0.0.0"
plugin_port = '50052'


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(f'{plugin_host}:{plugin_port}') as channel:
        stub = cli_plugin_pb2_grpc.CLIStub(channel)
        print("-------------- Discover --------------")
        results = stub.Discover(cli_plugin_pb2.DiscoverRequest())
        print(results)

        print("-------------- Exec --------------")
        for x in stub.Exec(cli_plugin_pb2.ExecRequest()):
            print(x)


if __name__ == '__main__':
    logging.basicConfig()
    run()
