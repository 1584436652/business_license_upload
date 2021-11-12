from openpyxl import Workbook


wb = Workbook()
ws = wb.active
ws.append(["公司名称", "核准日期", "是否和最新的核准日期一致", "法人", "是否和最新的法人一致",
           "公司地址", "邮编", "是否和最新的地址一致", "是否经营异常"])


def company_table(rows, data: dict):
    """
    需传进公司， 核准日期， 法人， 公司地址， 邮编， 经营情况
    :param rows:
    :param data:
    :return:
    """
    ws[f"A{rows}"] = data["company_name"]
    ws[f"B{rows}"] = data["date_of_establishment"]
    ws[f"C{rows}"] = data["logic_data"]
    ws[f"D{rows}"] = data["legal_person"]
    ws[f"E{rows}"] = data["logic_person"]
    ws[f"F{rows}"] = data["address"]
    ws[f"G{rows}"] = data["post_code"]
    ws[f"H{rows}"] = data["logic_address"]
    ws[f"I{rows}"] = data["business_conditions"]
    wb.save("./test.xlsx")

