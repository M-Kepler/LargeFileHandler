# -*-coding:utf-8-*-

import zmq
from datetime import datetime
from handler import DataHandler
from const import Config as cfg


class Client(object):
    def __init__(self):
        self._receiver = None
        self._sink = None
        self._context = zmq.Context()
        self._init_sinker_socket()
        self._init_receiver_socket()

    def _init_receiver_socket(self):
        """
        init connection to server
        """
        self._receiver = self._context.socket(zmq.PULL)
        # self._receiver.setsockopt(zmq.SNDTIMEO, cfg.CLIENT_SNDTIMEO)
        # self._receiver.setsockopt(zmq.RCVTIMEO, cfg.CLIENT_RCVTIMEO)
        self._receiver.connect(cfg.SERVER_ADDR)

    def _init_sinker_socket(self):
        """
        init connection to sinker
        """
        self._sender = self._context.socket(zmq.PUSH)
        # self._sender.setsockopt(zmq.SNDTIMEO, cfg.CLIENT_SNDTIMEO)
        # self._sender.setsockopt(zmq.RCVTIMEO, cfg.CLIENT_RCVTIMEO)
        self._sender.connect(cfg.SINK_ADDR)

    def receive_from_server(self):
        return self._receiver.recv()

    def send_to_sink(self, data):
        dt = datetime.now()
        print("[{}] send handle result({} bytes) to sinker".format(
            dt.strftime("%Y-%m-%d %H:%M:%S"), len(data)))
        self._sender.send(data)


def main():
    print("client listening ...")
    client = Client()
    data_handler_api = DataHandler()
    while True:
        msg = client.receive_from_server()

        # handling msg
        result = data_handler_api.work(msg)
        # FIXME 异步IO

        # send results to sink
        client.send_to_sink(result)


if __name__ == "__main__":
    main()
