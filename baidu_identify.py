import requests
import base64
import requests

from datetime import datetime
from utils import file_size
'''
营业执照识别
'''


def get_access_token():
    """
    client_id 为官网获取的AK
    client_secret 为官网获取的SK
    获取access_token
    """
    params = {
        "grant_type": "client_credentials",
        "client_id": "DVOep9tBuMwb20bvGDd4erBY",
        "client_secret": "tTrGGnTnGnuwAEZY4DQGNMUsKRETRYUD"
    }
    access_token_url = 'https://aip.baidubce.com/oauth/2.0/token?'
    response = requests.get(access_token_url, params=params)
    if response:
        return response.json()["access_token"]


def par(request_url, img):
    if "business_license" in request_url:
        return {"image": img}
    elif "idcard" in request_url:
        return {"id_card_side": "front", "image": img}


def recognition(img_path, access_token, request_url):
    """
    营业执照api https://aip.baidubce.com/rest/2.0/ocr/v1/business_license
    身份证api https://aip.baidubce.com/rest/2.0/ocr/v1/idcard
    :param img_path:
    :param access_token:
    :param request_url:
    :return:
    """
    file_size(img_path)
    # 二进制方式打开图片文件
    with open(img_path, 'rb') as f:
        img = base64.b64encode(f.read())
    # api不同请求参数有差异，需要判断
    access_token = access_token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=par(request_url, img), headers=headers)
    if response:
        return response.json()


def get_license(json_data):
    """
    解析营业执照json
    :param json_data:  识别的json数据
    :return:
    """
    result = json_data["words_result"]
    # 单位名称
    company_name = result["单位名称"].get("words")
    # 社会信用代码
    social_credit_code = result["社会信用代码"].get("words")
    # 法人
    legal_person = result["法人"].get("words")
    # 成立日期
    date_of_establishment = result["成立日期"].get("words")
    # 地址
    address = result["地址"].get("words")
    return {
        "company_name": company_name,
        "social_credit_code": social_credit_code,
        "legal_person": legal_person,
        "date_of_establishment": datetime.strptime(date_of_establishment, "%Y年%m月%d日"),
        "address": address,
    }


def get_id_card(id_card_json):
    """
    解析身份证正面json数据
    :param id_card_json:
    :return:
    """
    result = id_card_json["words_result"]
    # 姓名
    name = result["姓名"]["words"]
    # 民族
    ethnic = result["民族"]["words"]
    # 住址
    living = result["住址"]["words"]
    # 公民身份号码
    citizen_id_number = result["公民身份号码"]["words"]
    # 出生
    born = result["出生"]["words"]
    # 性别
    sex = result["性别"]["words"]
    return {
        "name": name,
        "ethnic": ethnic,
        "living": living,
        "citizen_id_number": citizen_id_number,
        "born": born,
        "sex": sex,
    }


def get_id_card_anti(id_card_json):
    """
        解析身份证反面json数据
        :param id_card_json:
        :return:
    """
    result = id_card_json["words_result"]
    # 失效日期
    expiration_date = result["失效日期"]["words"]
    # 签发机关
    issuing_authority = result["签发机关"]["words"]
    # 签发日期
    date_of_issue = result["签发日期"]["words"]
    return {
        "expiration_date": expiration_date,
        "issuing_authority": issuing_authority,
        "date_of_issue": date_of_issue,
    }


if __name__ == '__main__':
    token = get_access_token()
    data = recognition('柳林县荞歌红电子商务有限公司.png', token, "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license")
    print(data)
    # print(get_id_card(data))
