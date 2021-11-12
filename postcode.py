import re
from base64 import b64encode
from datetime import datetime

from crawler_base import CrawlerBase


class PostCode(CrawlerBase):

    @staticmethod
    def key_decrypt():
        """
        重写请求参数key的加密方式
        b64加密
        """
        text = "youbiankuyoubianku"
        keys = ''.join([datetime.now().strftime("%Y-%m-%d"), text])
        key = b64encode(keys.encode())
        key = re.findall(r"b'(.*?)'", str(key), re.S)[0]
        return key

    def parse_code(self, post_address):
        """
        post_address: 地址
        获取邮编
        """
        params = {
            "key": self.key_decrypt(),
            "address": post_address
        }
        code_res = self.make_response(url=self.url, headers=self.headers, params=params, method='GET')
        results = code_res.json()
        try:
            postcode = results["results"][0].get("postcode")
            return postcode
        except IndexError:
            print("很抱歉！该查询暂无结果！地址可能太长了")
            return "很抱歉！该查询暂无结果！地址可能太长了"


if __name__ == '__main__':
    post = PostCode("https://www.youbianku.cn/api/youbianku_zhannei_search.php?")
    address = "浙江省湖州市安吉县昌硕街道安吉大道589号"
    post.parse_code(address)


