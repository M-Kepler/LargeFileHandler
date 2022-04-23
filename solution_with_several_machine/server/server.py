# -*-coding:utf-8-*-

import zmq
from file_handler import FileHandler
from const import ServerCfg as const


class Server(object):

    def __init__(self):
        self._sender = None
        self._sink = None
        self._init_zmq()

    def _init_zmq(self):
        context = zmq.Context()
        self._sender = context.socket(zmq.PUSH)
        self._sender.bind(const.ADDR)

        self._sink = context.socket(zmq.PUSH)
        self._sink.connect(const.ADDR)

    def send_to_sinker(self, data):
        self._sink.send_string(data)

    def _send_to_worker(self, data):
        self._sender.send_string(data)

    def handler(self, data):
        print("sending %s bytes to worker" % len(data))
        self._send_to_worker(data)


def main():
    api = Server()

    # connect sink
    api.send_to_sinker("hello sinker")

    file_handle_api = FileHandler(
        const.INPUT_FILE, const.CHUNK_SIZE, api.handler)

    mission_cnt = 0
    for chunk_start, chunk_size in file_handle_api.chunkify():
        mission_cnt += 1
        print("work with chunk: [%s, %s]" %
              (chunk_start, chunk_start + chunk_size))

        # FIXME 这里只有发送出去后，才能继续处理下一块
        file_handle_api.work(chunk_start, chunk_size)

    print("distribute [{} missions] finish.".format(mission_cnt))


if __name__ == "__main__":
    main()
