# -*- coding:utf-8 -*-

from datetime import datetime
from decimal import Decimal

RESULT = "./result.txt"


def handle(id: str, symbol: str, price: Decimal, quantity: Decimal, type: str,
           dt: datetime) -> str:
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


pass
