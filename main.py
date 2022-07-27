#!-*- coding:utf-8

import pandas as pd
import logging
from src import HugeGraphRestClient

pd.options.display.width = 200
# pd.options.display.max_colwidth = 50
pd.options.display.max_columns = 20
pd.options.display.max_rows = 50

# init log for file and console
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename="data/hgclient.log", level=logging.INFO, format=log_format)
console = logging.StreamHandler(None)
console.setFormatter(logging.Formatter(log_format, None, "%"))
logging.root.addHandler(console)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# url_base = "http://10.14.139.71:8085/graphspaces/DEFAULT/graphs/hugegraph/"
url_base = "http://10.14.139.69:8085/graphspaces/DEFAULT/graphs/hugegraph/"
auth = ("admin", "admin")


# url_base = "http://10.14.139.70:8080/graphs/hugegraph/"
# auth = None

# depth_list = [1, 2, 3, 6, 23]
depth_list = [1, 2, 3]


def export_to_result(vid, depth, r, result):
    if vid not in result:
        result[vid] = {}

    if "measure" in r:
        m = r['measure']
        iters = int(1000 * (m['edge_iters'] + m['vertice_iters']) / m['cost'])
        logger.info("vid: {} depth: {} count: {}  iters/s: {}  {}".format(vid, depth, len(r['vertices']), iters, m))
        result[vid].update({
            'cost-{}'.format(depth): m['cost'],
            'count-{}'.format(depth): len(r['vertices']),
            'iters/s-{}'.format(depth): iters})
    else:
        logger.error("failed: {}".format(r))


def dump_result(result, depth):
    df = pd.DataFrame(result).T
    df.loc['avg'] = df.mean().astype(dtype="int32")
    logger.info("dumping result {}\n{}".format(depth, df))


def test_twitter_kout_get():

    logging.info("start kout-get({}) test. server={}".format(depth_list, url_base))
    client = HugeGraphRestClient(url_base, auth)

    vids = [20727483, 50329304, 26199460, 1177521, 27960125,
            30440025, 15833920, 15015183, 33153097, 21250581]
    # vids = [30440025, 15833920, 15015183, 33153097, 21250581]

    max_cap = 100000000
    result = {}
    for depth in depth_list:
        for vid in vids:
            r = client.do_kout_get({
                "source": vid,
                "max_depth": depth,
                "nearest": True,
                "max_degree": max_cap,
                "capacity": max_cap,
                "limit": max_cap,
                "concurrent": False
            })

            r['size'] = len(r['vertices'])
            export_to_result(vid, depth, r, result)

        dump_result(result, depth)


def test_twitter_kout_post():
    client = HugeGraphRestClient(url_base, auth)

    vids = [20727483, 50329304, 26199460, 1177521, 27960125,
            30440025, 15833920, 15015183, 33153097, 21250581]

    # 接口只支持最多 2000万
    max_cap = 20000000
    result = {}
    for depth in depth_list:
        for vid in vids:
            r = client.do_kout_post({
                "source": vid,
                "steps": {
                    "direction": "BOTH",
                    "max_degree": max_cap,
                    "skip_degree": max_cap
                },
                "max_depth": depth,
                "nearest": True,
                "limit": max_cap,
                "with_vertex": False,
                "with_path": False,
                "count_only": True
            })

            export_to_result(vid, depth, r, result)

        dump_result(result, depth)


if __name__ == '__main__':
    test_twitter_kout_get()
    # test_twitter_kout_post()
