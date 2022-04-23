# -*- coding:utf-8 -*-

import os
import math

# workspace path
WORK_DIR = os.path.curdir

# input file
INPUT_FILE = os.path.join(WORK_DIR, "input.txt")


# result output
OUPUT_FILE = os.path.join(WORK_DIR, "result.txt")

# each file size 100 GB (cause each machine support 128 GB memory)
# CHUNK_SIZE = 1024 * 1024 * 1024
# XXX FOR DEBUG
CHUNK_SIZE = 1 * 1024 * 1024
