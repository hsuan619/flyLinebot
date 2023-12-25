# import pygsheets

# auth_file = "D:/SideProject/mysite/tourbot/credentials.json"
# gc = pygsheets.authorize(service_file=auth_file)

# # setting sheet
# sheet_url = "https://docs.google.com/spreadsheets/d/1OQOV7ZACMvKVglJ50sHTG7OAG_R3UbKa0TrDrg0V7u8/"
# sheet = gc.open_by_url(sheet_url)
# sheet_test01 = sheet.worksheet_by_title("tour1")
# # user = input("輸入訂單編號：")


# def getWholeValues(user):
#     try:
#         if sheet_test01.find(user)[0]:
#             cell = sheet_test01.find(user)[0]
#             r = cell.row
#             dic = list((sheet_test01.get_all_records()[r - 2]).values())
#             return dic
#     except Exception:
#         print("此訂單號碼不存在")
# ==========
import pygsheets

auth_file = "flyline/credentials.json"
gc = pygsheets.authorize(service_file=auth_file)

# setting sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1OQOV7ZACMvKVglJ50sHTG7OAG_R3UbKa0TrDrg0V7u8/"
sheet = gc.open_by_url(sheet_url)
sheet_test01 = sheet.worksheet_by_title("student")
lastRow = len((sheet_test01).get_all_records()[0].values())


def getWholeValues(user):
    try:
        cell_list = sheet_test01.find(user)  # 可用來查詢通一間公司
        # print(cell_list)
        if cell_list:
            r = int(cell_list[0].row)  # row=2
            c = int(cell_list[0].col)  # column = 1
            dic = sheet_test01.get_values(start=(r, c), end=(r, lastRow))[0]
            # print(dic)
            return dic
    except Exception:
        return "此訂單號碼不存在"


def getShopDetail(shop):
    try:
        cell_list = sheet_test01.find(shop)
        totalAmount = 0
        for item in cell_list:
            r = int(item.row)  # row=2
            c = int(item.col)  # column = 1
            totalAmount += int(
                (sheet_test01.get_values(start=(r, c - 1), end=(r, c - 1)))[0][0]
            )
        # print(totalAmount)

        orderNum = len(cell_list)
        return [orderNum, totalAmount]

    except Exception:
        return 0
