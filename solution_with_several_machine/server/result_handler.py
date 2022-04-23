# -*- coding:utf-8 -*-

import json
from datetime import datetime
from decimal import Decimal
from const import SinkerCfg as const


class ResultHandler(object):
    def __init__(self):
        pass

    def _handle(self, id: str, symbol: str, price: Decimal, quantity: Decimal,
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

    def data_handler(self, chunk_data):
        """
        handle file data
        """
        dt = datetime.now()
        print("[{}] handling {} bytes message".format(
            dt.strftime("%Y-%m-%d %H:%M:%S"), len(chunk_data)))
        results = []
        for line in chunk_data.splitlines():
            try:
                line_content = json.loads(line)
                result = self._handle(**line_content)
            except Exception as ex:
                print("handle line with error: {}".format(ex))
            else:
                results.append(result + "\n")

        with open(const.OUPUT_FILE, "a+") as fd:
            fd.writelines(results)
