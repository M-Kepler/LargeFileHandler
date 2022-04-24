# -*- coding:utf-8 -*-

import os
import json
from datetime import datetime
from decimal import Decimal


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
