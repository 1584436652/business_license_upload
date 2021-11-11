import requests
from retry import retry
from lxml import etree

from Ua import ua
import config


class Enterprise(object):

    @property
    def link_config(self):
        ulr = "https://www.qcc.com/web/search?"
        headers = {
            'User-Agent': ua(),
            "cookie": config.LINK_COOKIE
        }
        return [ulr, headers]

    @property
    def detail_config(self):
        return {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/92.0.4515.159 Safari/537.36",
            "cookie": config.DETAIL_COOKIE
        }

    @staticmethod
    def key(key):
        return {
            "key": key
        }

    @retry(tries=3, delay=10)
    def make_response(self, url, headers, params=None):
        res = requests.get(url, headers=headers, params=params)
        res.encoding = "utf-8"
        print(f"状态码：{res.status_code}")
        assert res.status_code == 200
        return res.text

    def parse_link(self, link_res):
        link_html = etree.HTML(link_res)
        link = link_html.xpath('//div[@class="maininfo"]/a[1]/@href')[0]
        print(link)
        return link

    def parse_detail(self, detail_res):
        detail_html = etree.HTML(detail_res)
        items = detail_html.xpath('//section[@id="cominfo"]/div[2]/table')
        for item in items:
            # 核准日期
            approved_date = item.xpath('./tr[3]/td[6]/text()')[0]
            # 法人
            legal_person = item.xpath('./tr[2]/td[2]//span[@class="cont"]/span/span/a/text()')[0]
            # 注册地址
            registered_address = item.xpath('./tr[9]/td[2]//a[@class="text-dk copy-value"]/text()')[0]
            # 地区
            area = item.xpath('./tr[6]/td[6]/text()')[0]
            return {
                "approved_date": approved_date,
                "legal_person": legal_person,
                "registered_address": registered_address,
                "area": area
            }

    def main(self):
        keys = "安吉蓝城电子商务有限公司"
        res = self.make_response(self.link_config[0], self.link_config[1], self.key(keys))
        link = self.parse_link(res)
        detail = self.make_response(link, self.detail_config)
        print(self.parse_detail(detail))


if __name__ == '__main__':
    tian = Enterprise()
    tian.main()
