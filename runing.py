# from baidu_identify import get_access_token
# from baidu_identify import recognition
# from baidu_identify import get_license
# from tianyancha import Enterprise
# from postcode import PostCode
# from utils import walk_file
# from table import company_table
#
# import time
#
#
# def run():
#     # 获取百度识别的access_token
#     token = get_access_token()
#     for picture in walk_file():
#         # 返回二进制图片文件识别后的json
#         data = recognition(picture, token, "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license")
#         # 获取相对应的字段返回一个字典
#         messages = get_license(data)
#         # print(messages)
#         en = Enterprise()
#         # 获取企企查企业信息
#         find = en.main(messages["company_name"])
#         print(find)
#         post = PostCode("https://www.youbianku.cn/api/youbianku_zhannei_search.php?")
#         # 邮编
#         post_code = post.parse_code(messages["address"])
#         for k, v in find.items():
#             messages[k] = v
#         messages["post_code"] = post_code
#         print(messages)
#         yield messages
#
#
# def main():
#     rows = 2
#
#     for data in run():
#         print(f"my data{data}")
#         table_data = dict()
#         # 公司
#         table_data["company_name"] = data["company_name"]
#         # 核准日期
#         table_data["date_of_establishment"] = data["date_of_establishment"].strftime("%Y-%m-%d")
#         if data["date_of_establishment"] == data["approved_date"]:
#             table_data["logic_data"] = "是"
#         else:
#             table_data["logic_data"] = "否"
#         # 法人
#         table_data["legal_person"] = data["legal_person"]
#         if data["legal_person"] == data["legal_persons"]:
#             table_data["logic_person"] = "是"
#         else:
#             table_data["logic_person"] = "否"
#         # 公司地址
#         table_data["address"] = data["address"]
#         # 邮编
#         table_data["post_code"] = data["post_code"]
#         if data["address"] == data["registered_address"]:
#             table_data["logic_address"] = "是"
#         else:
#             table_data["logic_address"] = "否"
#         # 经营情况
#         table_data["business_conditions"] = "暂时还未实现"
#         table_data["registered_address"] = data["registered_address"]
#         company_table(rows, table_data)
#         rows += 1
#         print(table_data)
#         time.sleep(10)
#         print('\n')
#
#
# if __name__ == '__main__':
#     main()
