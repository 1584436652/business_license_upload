import requests
from retry import retry

from Ua import ua


class CrawlerBase:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': ua(),
            'Referer': 'https://www.youbianku.com/'
        }

    @retry(tries=3, delay=10)
    def make_response(self, params=None, **kwargs):
        _method = "GET" if not kwargs["method"] else kwargs["method"]
        if _method == "GET":
            res = requests.get(kwargs["url"], headers=kwargs["headers"], params=params)
        else:
            res = requests.post(kwargs["url"], headers=kwargs["headers"], data=kwargs["data"])
        res.encoding = "utf-8"
        assert res.status_code == 200
        return res

