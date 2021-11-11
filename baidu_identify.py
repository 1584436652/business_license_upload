import requests
import base64
import requests
'''
营业执照识别
'''


def get_access_token():
    """
    client_id 为官网获取的AK
    client_secret 为官网获取的SK
    获取access_token
    """
    access_token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
                       '&client_id=DVOep9tBuMwb20bvGDd4erBY&client_secret=tTrGGnTnGnuwAEZY4DQGNMUsKRETRYUD'
    response = requests.get(access_token_url)
    if response:
        return response.json()["access_token"]


def recognition(img_path, access_token):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license"
    # 二进制方式打开图片文件
    with open(img_path, 'rb') as f:
        img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = access_token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        return response.json()


def get_detail(json_data):
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
        "date_of_establishment": date_of_establishment,
        "address": address,
    }


if __name__ == '__main__':
    token = get_access_token()
    data = recognition('安吉蓝城电子商务有限公司.jpeg', token)
    print(get_detail(data))
