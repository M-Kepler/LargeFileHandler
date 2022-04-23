# -*- coding:utf-8 -*-

"""
Author       : M_Kepler
EMail        : m_kepler@foxmail.com
Last modified: 2022-04-23 12:10:25
Filename     : largeFileHandler.py
Description  : large file handler
"""

import datetime
import json
import math
import multiprocessing as mp
import os
from decimal import Decimal

import const


def handle(id: str, symbol: str, price: Decimal, quantity: Decimal, type: str,
           datetime: datetime) -> str:
    """ You need to write the result of the handle function to another text
    file named result.txt, and feel free to write the result to the result.txt,
    you can write it out of order.

    it is so easy if you process this file line by line

    Params:
        id:       - uuid, it is unique in this file.
        symbol:   - symbol
        price:    - the price of the symbol
        quantity: - the quantity of the symbol
        type:     - the type,
                    the optional value may be stock, feature, option, fund.
        dt:       - the datetime of the current line

    Returns:
        return string.

    Raises:
        pass
    e.g.::
        pass

    """
    return json.dumps({
        "id": id,
        "symbol": symbol,
        "price": price,
        "quantity": quantity,
        "type": type,
        "datetime": datetime
    })


def line_handler(chunk_data):
    """
    handle file data
    """
    results = []
    for line in chunk_data.splitlines():
        try:
            line_content = json.loads(line)
            result = handle(**line_content)
        except Exception as ex:
            print("handle {} with error: {}".format(line, ex))
        else:
            results.append(result + "\n")

    with open(const.OUPUT_FILE, "a+") as fd:
        fd.writelines(results)


class FileHandler(object):
    """
    large file handler
    """

    def __init__(self, input_file, callback):
        """
        :param input_file  - big file path
        :param callback    - function to handle each line of $input_file
        """
        self._input_file = input_file
        # for all process load memory
        self._chunk_size = math.ceil(const.CHUNK_SIZE / mp.cpu_count())
        self._callback = callback

    @property
    def _input_file_size(self):
        """
        get the size of input file (bytes)

        :return input_file_size
        """
        return os.stat(self._input_file).st_size

    def _chunkify(self):
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

                # XXX for log progress
                progress += (chunk_end - chunk_start)
                print('{0} MB of {1} MB bytes read ({2}%)'.format(
                    progress / 1024 / 1024, file_end / 1024 / 1024,
                    int(progress / file_end * 100)))

                yield chunk_start, chunk_end - chunk_start
                if chunk_end > file_end:
                    break

    def worker(self, chunk_start, chunk_size):
        """
        do_something with input file chunk
        """
        with open(self._input_file) as fd:
            fd.seek(chunk_start)
            chunk_data = fd.read(chunk_size)
            # FIXME 阻塞
            self._callback(chunk_data)

    def run(self):
        """
        handle file with multi process
        """

        pool = mp.Pool(mp.cpu_count())
        jobs = []
        for chunk_start, chunk_size in self._chunkify():
            jobs.append(pool.apply_async(
                self.worker, (chunk_start, chunk_size)))

        # do work with chunk
        for job in jobs:
            job.get()

        pool.close()


def main():
    if os.path.exists(const.OUPUT_FILE):
        os.remove(const.OUPUT_FILE)

    api = FileHandler(const.INPUT_FILE, line_handler)
    api.run()


if __name__ == "__main__":
    main()
