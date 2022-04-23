# -*-coding:utf-8-*-

import zmq
import time


def main():
    context = zmq.Context()

    receiver = context .socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")

    sender = context.socket(zmq.PUSH)
    sender .connect("tcp://localhost:5558")

    while 1:
        s = receiver.recv()
        print("worker 1 receive mission cost {} seconds".format(s))

        # handling mission
        time.sleep(int(s))

        # send results to sink
        sender.send_string(
            "worker 1 has finished mission, cost {} seconds".format(s))


if __name__ == "__main__":
    main()
