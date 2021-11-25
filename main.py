import time

from baidu_identify import get_access_token, get_id_card, get_id_card_anti
from baidu_identify import recognition
from baidu_identify import get_license
from tianyancha import Enterprise
from postcode import PostCode
from utils import set_files
from table import company_table


def image_information():
    # 获取百度识别的access_token
    token = get_access_token()
    for k, v in set_files().items():
        mess = []
        for v_pic in v:
            if "公司" in v_pic:
                print(v_pic)
                # 返回二进制图片文件识别后的json
                data = recognition(v_pic, token, "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license")
                # 获取相对应的字段返回一个字典
                messages_gs = get_license(data)
                mess.append(messages_gs)
            else:
                print(v_pic)
                data = recognition(v_pic, token, "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard")
                data_w = data["words_result"]
                if "民族" in data_w:
                    messages_id_positive = get_id_card(data)
                    mess.append(messages_id_positive)
                elif "失效日期" in data_w:
                    messages_anti = get_id_card_anti(data)
                    mess.append(messages_anti)
            time.sleep(1.5)
        yield mess


def merge_information(merge):
    messages = {}
    for dicts in merge:
        for k, v in dicts.items():
            if k not in messages:
                messages[k] = v
    en = Enterprise()
    # 获取企企查企业信息
    find = en.main(messages["company_name"])
    post = PostCode("https://www.youbianku.cn/api/youbianku_zhannei_search.php?")
    # 获取邮编
    post_code = post.parse_code(messages["address"])
    for k, v in find.items():
        messages[k] = v
    messages["post_code"] = post_code
    return messages


def main():
    rows = 2
    for me in image_information():
        data = merge_information(me)
        print(data)
        table_data = dict()
        # 公司
        table_data["company_name"] = data["company_name"]
        # 核准日期
        table_data["date_of_establishment"] = data["date_of_establishment"].strftime("%Y-%m-%d")
        if data["date_of_establishment"] == data["approved_date"]:
            table_data["logic_data"] = "是"
        else:
            table_data["logic_data"] = "否"
        # 法人
        table_data["legal_person"] = data["legal_person"]
        if data["legal_person"] == data["legal_persons"]:
            table_data["logic_person"] = "是"
        else:
            table_data["logic_person"] = "否"
        # 公司地址
        table_data["address"] = data["address"]
        # 邮编
        table_data["post_code"] = data["post_code"]
        if data["address"] == data["registered_address"]:
            table_data["logic_address"] = "是"
        else:
            table_data["logic_address"] = "否"
        # 经营情况
        table_data["business_conditions"] = data["business_conditions"]
        table_data["registered_address"] = data["registered_address"]
        table_data["name"] = data["name"]
        table_data["ethnic"] = data["ethnic"]
        table_data["sex"] = data["sex"]
        table_data["living"] = data["living"]
        table_data["citizen_id_number"] = data["citizen_id_number"]
        table_data["issuing_authority"] = data["issuing_authority"]
        table_data["date_of_issue"] = data["date_of_issue"]
        table_data["expiration_date"] = data["expiration_date"]
        company_table(rows, table_data)
        rows += 1
        print("保存成功")
        time.sleep(10)
        print('\n')


if __name__ == '__main__':
    main()
