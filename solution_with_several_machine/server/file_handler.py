# -*- coding:utf-8 -*-

""" big file handler
split file into serial chunk,
and call $callback function to handle it.
"""

import math
import multiprocessing as mp
import os

from const import ServerCfg as const


class FileHandler(object):
    """
    large file handler
    """

    def __init__(self, input_file, chunk_size, callback):
        """
        :param input_file  - big file path
        :param callback    - function to handle each line of $input_file
        """
        self._input_file = input_file
        # for all process load memory
        self._chunk_size = math.ceil(chunk_size / mp.cpu_count())
        self._callback = callback

    @property
    def _input_file_size(self):
        """
        get the size of input file (bytes)

        :return input_file_size
        """
        return os.stat(self._input_file).st_size

    def chunkify(self):
        """
        use generator to split big file into multi chunk

        :return (chunk_start, chunk_size)
        """

        file_end = self._input_file_size
        with open(self._input_file, "rb") as fd:
            chunk_end = fd.tell()
            progress = 0
            while True:
                chunk_start = chunk_end
                fd.seek(self._chunk_size, 1)
                fd.readline()
                chunk_end = fd.tell()

                progress += (chunk_end - chunk_start)
                print('{0} MB of {1} MB bytes read ({2}%)'.format(
                    progress / 1024 / 1024, file_end / 1024 / 1024,
                    int(progress / file_end * 100)))

                yield chunk_start, chunk_end - chunk_start
                if chunk_end > file_end:
                    break

    def work(self, chunk_start, chunk_size):
        """
        do_something with input file chunk
        """
        with open(self._input_file) as fd:
            fd.seek(chunk_start)
            chunk_data = fd.read(chunk_size)
            # FIXME 回调完成才能执行下一个任务？
            self._callback(chunk_data)


if __name__ == "__main__":
    def line_handler(line):
        print(line)

    api = FileHandler(const.INPUT_FILE, const.CHUNK_SIZE, line_handler)
    api.work(1, 161)
