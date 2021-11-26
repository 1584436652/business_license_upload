import requests
from random import choice
from datetime import datetime
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
            'User-Agent': ua(),
            "cookie": config.DETAIL_COOKIE
        }

    @staticmethod
    def key(key):
        return {
            "key": key
        }

    proxies = choice(config.PROXIES)

    @retry(delay=10)
    def make_response(self, url, headers, params=None):
        try:
            res = requests.get(url, headers=headers, params=params, proxies=self.proxies, timeout=3)
        except requests.exceptions.ProxyError as e:
            raise e
        res.encoding = "utf-8"
        assert res.status_code == 200
        return res.text

    @staticmethod
    def parse_link(link_res):
        link_html = etree.HTML(link_res)
        link = link_html.xpath('//div[@class="maininfo"]/a[1]/@href')[0]
        print(link)
        return link

    @staticmethod
    def parse_detail(detail_res):
        detail_html = etree.HTML(detail_res)
        manage = detail_html.xpath('//div[@class="nheader"]//div[@class="title"]/div[1]/span[1]/span/text()')[0]
        print(manage)
        items = detail_html.xpath('//section[@id="cominfo"]/div[2]/table')
        for item in items:
            # 核准日期
            approved_date = item.xpath('./tr[3]/td[6]/text()')[0]
            # 法人
            legal_persons = item.xpath('./tr[2]/td[2]//span[@class="cont"]/span/span/a/text()')[0]
            # 注册地址
            registered_address = item.xpath('./tr[9]/td[2]//a[@class="text-dk copy-value"]/text()')[0]
            # 地区
            area = item.xpath('./tr[6]/td[6]/text()')[0]
            return {
                "approved_date": datetime.strptime(approved_date, "%Y-%m-%d"),
                "legal_persons": legal_persons,
                "registered_address": registered_address,
                "area": area,
                "business_conditions": manage
            }

    def main(self, parameter_key):
        res = self.make_response(self.link_config[0], self.link_config[1], self.key(parameter_key))
        link = self.parse_link(res)
        detail = self.make_response(link, self.detail_config)
        return self.parse_detail(detail)


if __name__ == '__main__':
    tian = Enterprise()
    keys = "安吉蓝城电子商务有限公司"
    print(tian.main(keys))
