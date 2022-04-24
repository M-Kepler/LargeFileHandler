# -*-coding:utf-8-*-

"""
gather handle result from clients
and output final result to result.txt
"""

import asyncio
import os

import zmq
import zmq.asyncio

from const import SinkerCfg as cfg
from result_handle.result_handler import ResultHandler


class SinkServer(object):

    def __init__(self) -> None:
        self._receiver = None
        self._init_zmq()

    def _init_zmq(self):
        context = zmq.asyncio.Context()
        self._receiver = context.socket(zmq.PULL)
        self._receiver.bind(cfg.ADDR)

    async def rece_from_client(self):
        """
        receive handle result from client

        :return data
        """

        """
        XXX [DEL] FOR DEBUG
        dt = datetime.now()
        print("[{}] receive {} bytes to worker".format(
            dt.strftime("%Y-%m-%d %H:%M:%S"), len(data)))
        """
        data = await self._receiver.recv_string()
        return data


async def main():
    print("sink listening ...")
    sink_server = SinkServer()

    if os.path.exists(cfg.OUPUT_FILE):
        os.remove(cfg.OUPUT_FILE)

    while True:
        res_from_client = await sink_server.rece_from_client()

        # handle client result
        await ResultHandler().work(res_from_client)


if __name__ == "__main__":
    asyncio.run(main())
