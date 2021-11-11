import re
import requests
from base64 import b64encode
from datetime import datetime

from crawler_base import CrawlerBase


class PostCode(CrawlerBase):

    @staticmethod
    def key_decrypt():
        text = "youbiankuyoubianku"
        keys = ''.join([datetime.now().strftime("%Y-%m-%d"), text])
        key = b64encode(keys.encode())
        key = re.findall(r"b'(.*?)'", str(key), re.S)[0]
        print(key)
        return key

    def parse_code(self, address="浙江省湖州市安吉县昌硕街道安吉大道589号"):
        params = {
            "key": self.key_decrypt(),
            "address": address
        }
        code_res = self.make_response(url=self.url, headers=self.headers, params=params, method='GET')
        results = code_res.json()
        postcode = results["results"][0].get("postcode")
        print(postcode)
        return postcode


if __name__ == '__main__':
    post = PostCode("https://www.youbianku.cn/api/youbianku_zhannei_search.php?")
    post.parse_code()
    # print(post.key_decrypt())


