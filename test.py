#!-*- coding:utf-8

import time
import logging

# init log for file and console
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

logger = logging.getLogger(__name__)


def test():
    s = set()
    start = time.time()

    for i in range(0, 100000000):
        s.add(i)
    logger.info("test cost: {}".format(time.time() - start))
    s.copy()
    start = time.time()
    for i in range(0, 100000000):
        s.add(i)
    logger.info("test cost: {}".format(time.time() - start))


if __name__ == '__main__':
    test()
