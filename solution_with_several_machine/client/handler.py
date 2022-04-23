# -*- coding:utf-8 -*-

import os
import json
from datetime import datetime
from decimal import Decimal
import multiprocessing as mp


class DataHandler(object):

    def __init__(self):
        pass

    def handle(self, id: str, symbol: str, price: Decimal, quantity: Decimal,
               type: str, datetime: datetime) -> str:
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

    def work(self, line):
        """
        handle each line with function handle
        """
        try:
            """
            XXX [DEL] FOR DEBUG
            dt = datetime.now()
            print("[{}] pid: [{}] handling...".format(
                dt.strftime("%Y-%m-%d %H:%M:%S"), os.getpid()))
            """
            line_content = json.loads(line)
            return self.handle(**line_content)
        except Exception as ex:
            print("pid: [{}] handle line [{}] error: {}".format(
                os.getpid(), line, ex))

    async def run(self, socket):
        """
        handle file chunk, and return result

        :param socket - connection to sinker
        :return handle result list
        """

        data = await socket.receive_from_server()

        pool = mp.Pool(mp.cpu_count())
        jobs = []
        result = []
        for line in data.splitlines():
            jobs.append(pool.apply_async(self.work, (line, )))

        for job in jobs:
            handle_result = job.get()
            """
            XXX [DEL] FOR DEBUG
            dt = datetime.now()
            print("[{}] pid: [{}] sending...".format(
                dt.strftime("%Y-%m-%d %H:%M:%S"), os.getpid()))
            """
            await socket.send_to_sink(handle_result)
        pool.close()
