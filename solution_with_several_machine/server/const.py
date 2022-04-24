# -*- coding:utf-8 -*-

import os


class Config:

    # workspace path
    WORK_DIR = os.path.curdir


class ServerCfg(Config):

    # input file
    INPUT_FILE = os.path.join(Config.WORK_DIR, "input.txt")

    # each file size 100 GB (cause each machine support 128 GB memory)
    # CHUNK_SIZE = 100 * 1024 * 1024 * 1024
    # XXX FOR DEBUG 341.3M
    CHUNK_SIZE = 1024 * 1024 * 1024 / 3 / 10

    # record mission progress
    RUN_ID_PTH = os.path.join(Config.WORK_DIR, ".run/")

    RUN_ID_POSTFIX = ".run_id"

    # address
    ADDR = "tcp://127.0.0.1:5557"


class SinkerCfg(Config):
    # result output
    OUPUT_FILE = os.path.join(Config.WORK_DIR, "result.txt")

    # address
    ADDR = "tcp://127.0.0.1:5558"
