#!-*- coding:utf-8

import pandas as pd
import logging
import argparse
from src import HugeGraphRestClient
from testcase import kout, kneighbor

pd.options.display.width = 200
pd.options.display.max_columns = 20
pd.options.display.max_rows = 50

# init log for file and console
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename="log/hgclient.log", level=logging.INFO, format=log_format)
console = logging.StreamHandler(None)
console.setFormatter(logging.Formatter(log_format, None, "%"))
logging.root.addHandler(console)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

hosts = {
    "69": "http://10.14.139.69:8085/graphspaces/DEFAULT/graphs/{}/",
    "71": "http://10.14.139.71:8085/graphspaces/DEFAULT/graphs/{}/",
    "71s": "http://10.14.139.71:8081/graphspaces/DEFAULT/graphs/{}/",
}
auth = ("admin", "admin")

default_vids = [20727483, 50329304, 26199460, 1177521, 27960125,
            30440025, 15833920, 15015183, 33153097, 21250581]


methods = [
    "kout-get",
    "kout-post",
    "kneighbor-get",
    "kneighbor-post"
]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=methods, default=methods[0], type=str,
                        help="calling method for test, default is '{}'. available: {}".format(methods[0], methods))
    parser.add_argument("--depths", nargs="+", default=[1, 2, 3], type=int,
                        help="depth_list. default: '1 2 3'")
    parser.add_argument("--host", choices=hosts.keys(), default='69', type=str,
                        help="hugegraph server host, default is '69'")
    parser.add_argument("--graph", default='hugegraph', type=str,
                        help="graph name, default is 'hugegraph'")
    parser.add_argument("--max_cap", default=100000000, type=int,
                        help="max_capacity. default: 100000000")
    parser.add_argument("--vids", nargs="+", default=default_vids, type=int,
                        help="vid list. default: {}".format(default_vids))
    parser.add_argument("--strvid", default=False, type=bool,
                        help="use string vid, default is false")

    args = parser.parse_args()

    if args.strvid:
        args.vids = ['"' + str(v) + '"' for v in args.vids]

    url_base = hosts[args.host].format(args.graph)
    client = HugeGraphRestClient(url_base, auth)

    if args.method == 'kout-get':
        kout.test_twitter_get(client, args)
    elif args.method == 'kout-post':
        kout.test_twitter_post(client, args)
    elif args.method == 'kneighbor-get':
        kneighbor.test_twitter_get(client, args)
    elif args.method == 'kneighbor-post':
        kneighbor.test_twitter_post(client, args)
