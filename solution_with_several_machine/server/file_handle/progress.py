# -*- coding:utf-8 -*-

"""
handle mission progress
"""

import json
import os
from const import ServerCfg as cfg


class Progress(object):
    def __init__(self):
        self._progress_list = self._get_progress()

    def is_mission_finish(self, mission_size):
        """
        is all mission finish

        :param mission_size    - size of mission file
        :return True or False
        """
        curr_progress = sum([
            (x[1] - x[0] + 1)
            for x in self._progress_list])
        return mission_size < curr_progress

    def is_chunk_handled(self, chunk):
        """
        is chunk already handled.

        :param chunk            - mission chunk range
        """
        return chunk in self._progress_list

    def _get_progress(self):
        """
        get progress sum from run id files
        """

        progress_list = []

        # mkdir run id store path
        if not os.path.exists(cfg.RUN_ID_PTH):
            os.mkdir(cfg.RUN_ID_PTH)

        for _, _, files in os.walk(cfg.RUN_ID_PTH):
            for file in files:
                if not file.endswith(cfg.RUN_ID_POSTFIX):
                    continue

                with open(os.path.join(cfg.RUN_ID_PTH, file), "r") as fd:
                    for line in fd.readlines():
                        progress_list.append(json.loads(line))

        # latest mission progress
        print("\n===== latest mission progress: {} =====\n".format(
            progress_list))

        return progress_list

    def update_progress(self, chunk_start, chunk_size):
        """
        update current mission progress
        """
        pid = os.getpid()
        run_id_pth = os.path.join(
            cfg.RUN_ID_PTH,
            str(pid) + cfg.RUN_ID_POSTFIX)

        with open(run_id_pth, "a+") as fd:
            new_progress = chunk_start + chunk_size

            print("pid:[{}] progress [{}, {}] done".format(
                pid, chunk_start, new_progress))

            fd.write("[" + str(chunk_start) + "," + str(new_progress) + "]\n")
