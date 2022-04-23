# -*- coding:utf-8 -*-

import os

# workspace path
WORK_DIR = os.path.curdir

# input file
INPUT_FILE = os.path.join(WORK_DIR, "input.txt")


# result output
OUPUT_FILE = os.path.join(WORK_DIR, "result.txt")

# each file size 100 GB (cause each machine support 128 GB memory)
# CHUNK_SIZE = 100 * 1024 * 1024 * 1024

# XXX FOR DEBUG 341.3M
CHUNK_SIZE = 1024 * 1024 * 1024 / 3
