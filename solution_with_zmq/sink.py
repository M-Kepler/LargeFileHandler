# -*-coding:utf-8-*-

import zmq
import time


def main():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://localhost:5558")

    s = receiver.recv()
    print("handing mission result ...")

    start_tm = time.time()

    for task_item in range(10):
        s = receiver.recv_string()
        print(s)

    end_tm = time.time()
    print("workers work togeter, total cost {} seconds".format(end_tm - start_tm))


if __name__ == "__main__":
    main()
