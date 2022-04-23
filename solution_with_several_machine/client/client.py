# -*-coding:utf-8-*-

import os
import zmq
import asyncio
import zmq.asyncio
from datetime import datetime
from handler import DataHandler
from const import Config as cfg


class Client(object):
    def __init__(self):
        self._receiver = None
        self._sink = None
        self._context = zmq.asyncio.Context()
        self._init_sinker_socket()
        self._init_receiver_socket()

    def _init_receiver_socket(self):
        """
        init connection to server
        """
        self._receiver = self._context.socket(zmq.PULL)
        self._receiver.connect(cfg.SERVER_ADDR)

    def _init_sinker_socket(self):
        """
        init connection to sinker
        """
        self._sender = self._context.socket(zmq.PUSH)
        self._sender.connect(cfg.SINK_ADDR)

    async def receive_from_server(self):
        """
        receive data from server
        :return data
        """
        dt = datetime.now()
        data = await self._receiver.recv_string()
        print("[{}] pid: [{}] receive data ({} bytes) from server".format(
            dt.strftime("%Y-%m-%d %H:%M:%S"), os.getpid(), len(data)))
        return data

    async def send_to_sink(self, data):
        """
        send handle result to sink

        :param data - handle result
        """
        await self._sender.send_string(data)


async def main():
    print("client listening ...")
    client = Client()
    data_handler_api = DataHandler()
    while True:
        # handling msg
        await data_handler_api.run(client)


if __name__ == "__main__":
    asyncio.run(main())
