#!-*- coding:utf-8

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def dump_result(result, msg):
    df = pd.DataFrame(result).T
    df.loc['avg'] = df.mean().astype(dtype="int32")
    logger.info("dumping result {}\n{}".format(msg, df))


def export_to_result(vid, depth, r, result):
    if vid not in result:
        result[vid] = {}

    # print(r)

    if "measure" in r:
        m = r['measure']
        iter_count = m['edge_iters'] + m['vertice_iters'];
        iter_speed = int(1000 * iter_count / m['cost'])
        logger.info("vid: {} depth: {} count: {}  iters: {}  iters/s: {}  {}".format(
            vid, depth, r['size'], iter_count, iter_speed, m))
        result[vid].update({
            'cost-{}'.format(depth): m['cost'],
            'count-{}'.format(depth): r['size'],
            'iter-{}'.format(depth): iter_count,
            'iters/s-{}'.format(depth): iter_speed})
    else:
        logger.error("failed: {}".format(r))
