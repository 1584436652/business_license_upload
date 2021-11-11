import requests
from retry import retry

from Ua import ua


class CrawlerBase:
    def __init__(self, url):
        self.url = url

    @property
    def config(self):
        ulr = self.url
        headers = {
            'User-Agent': ua(),
        }
        return [ulr, headers]

    @retry(tries=3, delay=10)
    def make_response(self, url, headers, params=None):
        res = requests.get(url, headers=headers, params=params)
        res.encoding = "utf-8"
        print(f"状态码：{res.status_code}")
        assert res.status_code == 200
        return res.text


if __name__ == '__main__':
    pass