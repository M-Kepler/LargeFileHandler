# -*-coding:utf-8-*-

import zmq
import random


class LargeFileHandler(object):
    pass


def main():
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://localhost:5557")

    sink = context.socket(zmq.PUSH)
    sink.connect("tcp://localhost:5558")

    print("press enter when the workers are ready: ")
    _ = input()
    print("sending tasks to workers ...")
    sink.send_string("0")

    # 发送10个任务
    total_msec = 0
    for task_nbr in range(10):
        # 每个任务耗时为 N
        workload = random.randint(1, 5)
        total_msec += workload
        sender.send_string(u"%i" % workload)
    print("finish 10 mission cost: {} seconds".format(total_msec))


if __name__ == "__main__":
    main()
