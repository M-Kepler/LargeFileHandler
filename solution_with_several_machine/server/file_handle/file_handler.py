# -*- coding:utf-8 -*-
"""
Author       : M_Kepler
EMail        : m_kepler@foxmail.com
Last modified: 2022-04-23 12:10:25
Filename     : largeFileHandler.py
Description  : large file handler
"""

import math
import multiprocessing as mp
import os
import sys
import aiofiles

from const import ServerCfg
from file_handle.progress import Progress


class FileHandler(object):
    """
    large file handler
    """

    def __init__(self, input_file, callback):
        """
        :param input_file  - file path
        :param callback    - function to handle each line of $input_file
        """
        self._input_file = input_file
        self._progress_api = Progress()
        # for all process load memory
        self._chunk_size = math.ceil(ServerCfg.CHUNK_SIZE / mp.cpu_count())
        self._callback = callback

    @property
    def _input_file_size(self):
        """
        get the size of input file (bytes)

        :return input_file_size
        """
        file_size = os.stat(self._input_file).st_size
        print("===== input file size: {} =====\n".format(file_size))
        return file_size

    def chunkify(self):
        """
        use generator to split big file into multi chunk

        :return (chunk_start, chunk_size)
        """

        file_end = self._input_file_size
        with open(self._input_file, "rb") as fd:

            # check progress
            if self._progress_api.is_mission_finish(file_end):
                print("misssion already finished.\n")
                sys.exit(0)

            chunk_end = fd.tell()
            chunk_progress = 0
            while True:
                chunk_start = chunk_end
                fd.seek(self._chunk_size, 1)
                fd.readline()
                # the last chunk should be the end of file
                chunk_end = fd.tell() if fd.tell() <= file_end else file_end

                # chunk already handled.
                chunk_size = chunk_end - chunk_start
                if self._progress_api.is_chunk_handled([chunk_start, chunk_end]):
                    print("===== chunk [{}, {}] already handled.".format(
                        chunk_start, chunk_end))
                    continue

                # for log progress
                chunk_progress += (chunk_end - chunk_start)
                print('{0} MB of {1} MB bytes read ({2}%)'.format(
                    chunk_progress / 1024 / 1024, file_end / 1024 / 1024,
                    int(chunk_progress / file_end * 100)))

                yield chunk_start, chunk_size
                if chunk_end >= file_end:
                    print("\n===== file chunk done =====\n")
                    break

    async def worker(self, chunk_start, chunk_size):
        """
        work with input file chunk

        :param chunk_start - pointer of file content
        :param chunk_size  - size of parts os file
        """
        print("pid:[{}] warking between [{}, {}]".format(
            os.getpid(), chunk_start, chunk_start + chunk_size))

        async with aiofiles.open(self._input_file) as fd:
            fd.seek(chunk_start)
            chunk_data = await fd.read(chunk_size)
            await self._callback(chunk_data)
            self._progress_api.update_progress(chunk_start, chunk_size)
