# -*- coding:utf-8 -*-

from datetime import datetime

import aiofiles

from const import SinkerCfg as const


class ResultHandler(object):
    def __init__(self):
        pass

    async def work(self, data):
        """
        handle client result

        :param data message from client
        """

        """
        XXX [DEL] FOR DEBUG
        dt = datetime.now()
        print("[{}] handling {} bytes message".format(
            dt.strftime("%Y-%m-%d %H:%M:%S"), len(data)))
        """

        async with aiofiles.open(const.OUPUT_FILE, "a+") as fd:
            await fd.write(data + "\n")
