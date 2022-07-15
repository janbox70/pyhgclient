
import requests


class HugeGraphRestClient:
    def __init__(self, url_base, auth):
        self.url_base = url_base
        self.auth = auth

    def do_get(self, api, params):
        url = self.url_base + api
        r = requests.get(url, params, auth=self.auth)
        if r.status_code == 200:
            return r.json()
        print("get({}) failed({}): {}".format(url, r.status_code, r.content))
        return r

    def do_post(self, api, params):
        url = self.url_base + api
        r = requests.post(url, json=params, auth=self.auth)
        if r.status_code == 200:
            return r.json()
        print("post({}) failed({}): {}".format(url, r.status_code, r.content))
        return r

    def do_kout_get(self, params):
        r = self.do_get("traversers/kout", params)
        return r

    def do_kout_post(self, params):
        r = self.do_post("traversers/kout", params)
        return r
