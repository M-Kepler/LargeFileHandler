# -*-coding:utf-8-*-

"""
read file and split into several chunk
distribu chunk to clients for further processing
"""

import zmq
import asyncio
import zmq.asyncio
from datetime import datetime
from file_handle.file_handler import FileHandler
from const import ServerCfg as const


class Server(object):

    def __init__(self):
        self._sender = None
        self._init_zmq()

    def _init_zmq(self):
        context = zmq.asyncio.Context()
        self._sender = context.socket(zmq.PUSH)
        self._sender.bind(const.ADDR)

    async def handler(self, data):
        """
        send mission data to worker

        :param data
        """
        dt = datetime.now()
        print("[{}] send {} bytes to worker".format(
            dt.strftime("%Y-%m-%d %H:%M:%S"), len(data)))
        await self._sender.send_string(data)


async def main():
    api = Server()

    file_handle_api = FileHandler(
        const.INPUT_FILE, api.handler)

    mission_cnt = 0
    for chunk_start, chunk_size in file_handle_api.chunkify():
        mission_cnt += 1

        # send data to worker
        await file_handle_api.worker(chunk_start, chunk_size)

    print("distribute [{} missions] finish.".format(mission_cnt))


if __name__ == "__main__":
    asyncio.run(main())
