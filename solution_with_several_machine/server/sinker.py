# -*-coding:utf-8-*-

"""
result collector
"""

import zmq
import os
from result_handler import ResultHandler

from const import SinkerCfg as cfg


def init_zmq():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(cfg.ADDR)
    return socket


def main():

    if os.path.exists(cfg.OUPUT_FILE):
        os.remove(cfg.OUPUT_FILE)

    receiver = init_zmq()
    # print("got message {} from server, handle mission...".format(msg))
    while True:
        # summary handle result
        res_from_client = receiver.recv_string()
        # FIXME 异步 IO
        ResultHandler().data_handler(res_from_client)


if __name__ == "__main__":

    main()
