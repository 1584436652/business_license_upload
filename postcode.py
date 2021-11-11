import re
import json

from crawler_base import CrawlerBase


class PostCode(CrawlerBase):

    def parse(self):
        res = self.make_response(self.config[0], self.config[1])
        # print(res)
        keys = re.findall(r"type: 'POST',(.*?)dataType: 'json'", res, re.S)[0].strip().rstrip(',')
        key = re.findall(r"key: '(.*?)'", json.dumps(keys), re.S)[0]
        return key


if __name__ == '__main__':
    post = PostCode("https://www.youbianku.com/")
    print(post.parse())


