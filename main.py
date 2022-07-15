import pandas as pd
from src import HugeGraphRestClient

# url_base = "http://10.14.139.71:8085/graphspaces/DEFAULT/graphs/hugegraph/"
url_base = "http://10.14.139.69:8085/graphspaces/DEFAULT/graphs/hugegraphn/"
auth = ("admin", "admin")


def test_twitter_kout_get():
    client = HugeGraphRestClient(url_base, auth)

    vids = [20727483, 50329304, 26199460, 1177521, 27960125,
            30440025, 15833920, 15015183, 33153097, 21250581]

    max_cap = 100000000
    result = {}
    for depth in range(1, 3):
        for vid in vids:
            r = client.do_kout_get({
                "source": vid,
                "max_depth": depth,
                "nearest": True,
                "max_degree": max_cap,
                "capacity": max_cap,
                "limit": max_cap,
            })

            # print(r)
            if vid not in result:
                result[vid] = {}

            if "measure" in r:
                m = r['measure']
                print("vid: {}  count: {}  {}".format(vid, len(r['vertices']), m))
                result[vid].update({
                    'cost-{}'.format(depth): m['cost'],
                    'count-{}'.format(depth): len(r['vertices']),
                    'iters/s-{}'.format(depth): int(1000 * (m['edge_iters'] + m['vertice_iters']) / m['cost'])})
            else:
                print(r)

    df = pd.DataFrame(result).T
    df.loc['avg'] = df.mean().astype(dtype="int32")
    print(df)


def test_twitter_kout_post():
    client = HugeGraphRestClient(url_base, auth)

    vids = [20727483, 50329304, 26199460, 1177521, 27960125,
            30440025, 15833920, 15015183, 33153097, 21250581]

    # 接口只支持最多 2000万
    max_cap = 20000000
    result = {}
    for depth in range(1, 3):
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

            if vid not in result:
                result[vid] = {}

            if "measure" in r:
                # print(r)
                m = r['measure']
                print("vid: {}  count: {}  {}".format(vid, r['size'], m))
                result[vid].update({
                    'cost-{}'.format(depth): m['cost'],
                    'count-{}'.format(depth): r['size'],
                    'iters/s-{}'.format(depth): int(1000 * (m['edge_iters'] + m['vertice_iters']) / m['cost'])})
            else:
                print(r)

    df = pd.DataFrame(result).T
    df.loc['avg'] = df.mean().astype(dtype="int32")
    print(df)


if __name__ == '__main__':
    test_twitter_kout_get()
    # test_twitter_kout_post()
