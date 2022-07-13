
import requests


class HugeGraphRestClient:
    def __init__(self, url_base, auth):
        self.url_base = url_base
        self.auth = auth

    def do_get(self, api, params):
        r = requests.get(self.url_base + api, params, auth=self.auth)
        if r.status_code != 200:
            raise "requests get failed: {}".format(r.status_code)
        return r.json()

    def do_kout_get(self, params):
        r = self.do_get("traversers/kout", params)
        return r

