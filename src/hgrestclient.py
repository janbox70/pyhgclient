#!-*- coding:utf-8

import logging
import requests
import time

logger = logging.getLogger("HugeGraphRestClient")


class HugeGraphRestClient:
    def __init__(self, url_base, auth):
        self.url_base = url_base
        self.auth = auth

    def normalize(self, r, cost):
        # 开源 hugegraph无 measure，这里使用本地计时来代替
        if "measure" not in r:
            r['measure'] = {"type": "local", "cost": cost, "edge_iters": 0, "vertice_iters": 0}
        return r

    def do_get(self, api, params):
        url = self.url_base + api
        start = time.time()
        try:
            r = requests.get(url, params, auth=self.auth)
        except Exception as e:
            logger.error("get({}) failed with exception: {}".format(url, e))
            raise e
        end = time.time()
        if r.status_code == 200:
            return self.normalize(r.json(), int((end-start) * 1000))
        logger.error("get({}) failed({}): {}".format(url, r.status_code, r.content))
        return r

    def do_post(self, api, params):
        url = self.url_base + api
        start = time.time()
        try:
            r = requests.post(url, json=params, auth=self.auth)
        except Exception as e:
            logger.error("get({}) failed with exception: {}".format(url, e))
            raise e
        end = time.time()
        if r.status_code == 200:
            return self.normalize(r.json(), int((end-start) * 1000))
        logger.error("post({}) failed({}): {}".format(url, r.status_code, r.content))
        return r

    def do_kout_get(self, params):
        r = self.do_get("traversers/kout", params)
        return r

    def do_kout_post(self, params):
        r = self.do_post("traversers/kout", params)
        return r
