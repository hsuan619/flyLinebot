import pygsheets
import pandas as pd
import schedule
import time
from datetime import datetime, timedelta


auth_file = "flyline/flybot.json"
gc = pygsheets.authorize(service_file=auth_file)
sheet_id = "1KYsTpbF6eiTT3-GP3VFlXdiOWe8WwCa5z6ZA1XC1RKk"
sh = gc.open_by_key(sheet_id)


wks = sh.worksheet_by_title("course")
wks2 = sh.worksheet_by_title("teacher")


def setCourse(num, user):
    # If multiple numbers are provided, split them and update the worksheet for each number
    num_list = num.split(",")

    for n in num_list:
        row = (
            len(wks2.get_col(1, returnas="cell", include_empty=False)) + 1
        )  # Find the next available row
        n = n.strip()
        # print(n)
        wks2.update_values(f"A{row}", [[n]])  # Add the data to the next avai
        wks2.update_values(f"B{row}", [[user]])


def isExit(reList):
    reList = reList.split(",")  # list
    for n in reList:
        n = n.strip()
        if wks2.find(n):
            return True
        else:
            return False


def getDeatilByUser(id):
    results = wks2.find(id)
    reList = []
    for i in results:
        r = int(i.row)
        c = int(i.col)
        re = wks2.get_values(start=(r, c - 1), end=(r, c - 1))[0][0]
        reList.append(re)
    # getDetailByDate(reList)
    return reList
    # print(reList)
    # return re  # 取出課號+日期
    # getTargetDetail(re)


# def delUser(id):
#     results = wks2.find(id)
#     if results:
#         for i in results:
#             r = int(i.row)
#             c = int(i.col)
#             # print(r, c)
#             wks2.update_values(i.label, [[" "]])
#             wks2.update_values((r, c - 1), [[" "]])
#             wks2.delete_rows(r)
#             print("刪除成功")
#     else:
#         print("刪除失敗")


def delUser(id):
    rows = []
    results = wks2.find(id)
    if results:
        for i in results:
            r = int(i.row)
            rows.append(r)
        print(rows[0], r)  # 第一row及最後row
        # wks2.update_values(i.label, [[" "]])
        # wks2.update_values((r, c - 1), [[" "]])

        wks2.delete_rows(rows[0], r)  # 起始,結束
        print("刪除成功")
    else:
        print("刪除失敗")


def getUser(re):
    for r in re:
        target = wks2.find(r)
        for t in target:
            r = int(t.row)
            c = int(t.col)
            user = wks2.get_values(start=(r, c + 1), end=(r, c + 1))[0][0]
            return user


# list = getDeatilByUser("U40312c953c499d83cb749fc62140c42e")
# # print(getDeatilByUser("U40312c953c499d83cb749fc62140c42e"))
# print(getDetailByDate(list))


# ==========1225
# 持續檢查欄位是否有相近日期
# 再由日期對應課號找到userid
# 先找日期
# 找課號對應他給的試算表
# 取出內容
# 對應User傳通知


def get_next_day(date_string: str) -> str:
    """Return the next day as a formatted string (MM/DD)"""
    date_object = datetime.strptime(date_string, "%m/%d")
    next_day = date_object + timedelta(days=1)
    return next_day.strftime("%m/%d")


def get_pre_day(date_string: str) -> str:
    """Return the next day as a formatted string (MM/DD)"""
    date_object = datetime.strptime(date_string, "%m/%d")
    pre_day = date_object - timedelta(days=1)
    return pre_day.strftime("%m/%d")


def getToday():
    today = datetime.today().strftime("%m/%d")
    return today


def getDetailByDate(reList):  # 從課表抓詳細課程.
    resultList = ""
    for r in reList:
        results = wks.find(r)
        if results:
            # print(results[0].value)
            resultList = (results[0].value) + "\n" + resultList
            resultList = resultList.strip()
        else:
            print("沒有符合")
            return 0
    return resultList


def check_date_in_sheet():
    # 檢查試算表中的日期欄位
    try:
        # all_values = wks2.get_all_values()
        delExpireRow()
        next_day = get_next_day(getToday())
        # print(today, next_day)
        target = wks2.find(next_day)
        if target:
            re = []
            for t in target:
                re.append(t.value)
            print(re)
            return re
        else:
            print("今天無")

    except Exception:
        return 0


def delExpireRow():
    expireDate = get_pre_day(getToday())
    expireTarget = wks2.find(expireDate)
    if expireTarget:
        rows = []
        print(expireTarget)
        for t in expireTarget:
            r = int(t.row)
            rows.append(r)
        print(rows[0], r)  # 第一row及最後row
        wks2.delete_rows(rows[0], r)  # 起始,結束
        return 1
        # print(getToday())
        # print("刪除過期成功")
    else:
        return 0


# def notice(Userid, detail):
#     t = f"{Userid}您有課程在明天${detail}"
#     print(t)


# test============================================
# numAndDate = check_date_in_sheet()
# if numAndDate:
#     detail = getDetailByDate(numAndDate)
#     user = getUser(numAndDate)
#     print(f"id: {user} \ndetail: {detail}")
# else:
#     print("not find")


# user = check_date_in_sheet()[0]
# searchItem = check_date_in_sheet()[1]
