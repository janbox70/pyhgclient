#!-*- coding:utf-8

import logging
from util import dump_result, export_to_result


logger = logging.getLogger("kout")


def test_twitter_get(client, args):
    depth_list = args.depths
    max_cap = args.max_cap
    vids = args.vids
    logging.info("start {}({}) test for server={}\ndepths={}, max_cap={}, vids={}"
                 .format(args.method, depth_list, client.url_base, depth_list, max_cap, vids))

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

        dump_result(result, "{}-{}".format(args.method, depth))


def test_twitter_post(client, args):
    depth_list = args.depths
    max_cap = args.max_cap
    vids = args.vids
    logging.info("start {}({}) test for server={}\ndepths={}, max_cap={}, vids={}"
                 .format(args.method, depth_list, client.url_base, depth_list, max_cap, vids))

    # 接口只支持最多 2000万
    result = {}
    for depth in depth_list:
        for vid in vids:
            r = client.do_kout_post({
                "source": vid,
                "steps": {
                    "direction": "BOTH",
                    "max_degree": max_cap
                    # "skip_degree": max_cap
                },
                "max_depth": depth,
                "nearest": True,
                "limit": max_cap,
                "with_vertex": False,
                "with_path": False,
                "count_only": True
            })

            export_to_result(vid, depth, r, result)

        dump_result(result, "{}-{}".format(args.method, depth))

