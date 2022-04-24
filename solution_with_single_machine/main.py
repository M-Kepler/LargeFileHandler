# -*- coding:utf-8 -*-

"""
handle file with multi process
"""

import datetime
import json
import multiprocessing as mp
from decimal import Decimal

import const

from file_handler import FileHandler


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


def main():
    """
    if os.path.exists(const.OUPUT_FILE):
        os.remove(const.OUPUT_FILE)
    """

    handle_api = FileHandler(const.INPUT_FILE, line_handler)

    pool = mp.Pool(mp.cpu_count())
    jobs = []

    for chunk_start, chunk_size in handle_api.chunkify():
        jobs.append(pool.apply_async(
            func=handle_api.worker,
            args=(chunk_start, chunk_size)))

    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
