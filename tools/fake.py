# -*- coding:utf-8 -*-

import json
import sys
import datetime
import random
import time
import uuid
import multiprocessing

INPUT_FILE = "input.txt"

TYPES = ["stock", "feature", "option", "fund"]
MIN_TIME = datetime.datetime(2010, 1, 1, 0, 0, 0, 0)
MIN_TIME_TS = int(time.mktime(MIN_TIME.timetuple()))

MAX_TIME = datetime.datetime(2022, 4, 22, 0, 0, 0)
MAX_TIME_TS = int(time.mktime(MAX_TIME.timetuple()))


def fake_data(count):
    fake_data = list()

    for _ in range(count):
        random_time = datetime.datetime.fromtimestamp(
            random.randint(MIN_TIME_TS, MAX_TIME_TS))
        dt = str(random_time.strftime('%Y-%m-%d %H:%M:%S')) + \
            str(random.randint(1, 999))

        fake_data.append(json.dumps({
            "id": str(uuid.uuid4()),
            "symbol": "%06d" % random.randint(1, 999999) + ".XSHE",
            "price": round(random.uniform(1, 100), 2),
            "quantity": random.randint(1, 1000),
            "type": random.choice(TYPES),
            "datetime": dt
        }))

        fake_data.append("\n")

    with open(INPUT_FILE, "w") as fd:
        fd.writelines(fake_data)


def callback_func(content):
    with open(INPUT_FILE, "a+") as fd:
        line = str(content) + "\n"
        fd.write(line)


def worker():
    random_time = datetime.datetime.fromtimestamp(
        random.randint(MIN_TIME_TS, MAX_TIME_TS))
    dt = str(random_time.strftime('%Y-%m-%d %H:%M:%S')) + \
        str(random.randint(1, 999))
    return json.dumps(
        {
            "id": str(uuid.uuid4()),
            "symbol": "%06d" % random.randint(1, 999999) + ".XSHE",
            "price": round(random.uniform(1, 100), 2),
            "quantity": random.randint(1, 1000),
            "type": random.choice(TYPES),
            "datetime": dt
        })


def main():
    if len(sys.argv) < 2:
        print("""
        usage: python fake.py [fake_cnt]
        """)
        sys.exit(1)

    count = int(sys.argv[1])

    cpu_count = multiprocessing.cpu_count()
    p = multiprocessing.Pool(cpu_count)

    for _ in range(count):
        p.apply_async(worker, callback=callback_func)

    p.close()
    p.join()


if __name__ == "__main__":
    main()
