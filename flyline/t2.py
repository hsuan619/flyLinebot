import pygsheets
import pandas as pd
import re
import datetime
import schedule
import time

gc = pygsheets.authorize(service_file="D:/SideProject/flight/flyline/flybot.json")
# open the google spreadsheet
sh = gc.open_by_key("yuor sheet id")
wks = sh.worksheet_by_title("tour1")
gc2 = pygsheets.authorize(service_file="D:/SideProject/flight/flyline/flybot.json")
# open the google spreadsheet
sh2 = gc2.open_by_key("yuor sheet id")
# select the first worksheet
wks2 = sh2.worksheet_by_title("teacher")


def getCourseNum(userid):
    try:
        nums = wks2.find(userid)  # 找userId位置
        for i in nums:
            r = int(i.row)
            c = int(i.col)
            item = wks2.get_values(start=(r, c - 1), end=(r, c - 1))[0][0]
            return item  # 取出課號
            # print(item)
            # getDate(item)  # 丟到getCourses(item)取通知日期
        #     sch = res[0][2].split(",")
        #     print(sch)
        # # for info in sch:
        #     # 使用正則表達式來匹配日期和時間
        #     match = re.search(
        #         r"(\d{1,2}/\d{1,2})\(.+?\) (\d{1,2}:\d{2})-(\d{1,2}:\d{2})", info
        #     )
        #     if match:
        #         # 第一個匹配組是日期，第二和第三個匹配組是開始和結束時間
        #         date = match.group(1) #取對方課表的日期

    except Exception:
        return False


# 綁定後 從userid找課號
# 先取出此刻號有幾堂課and日期，再做
# 再tour李find tcinfo，取出日期
def getTargetDate(item):
    results = wks.find(item)
    results = results[0].value.split(",")  # 找到包含課號的第一個，再以","分割
    # print(results)
    for result in results:
        # print(result.strip())
        result = result.strip()
        getDate = result.split(
            " "
        )  # 一列以空格區分([0]課號[1]日期[2]時間) => C01-1 12/29(五) 19:00-22:00數學
        if item in getDate:
            # noticeTeacher(getDate[1])
            return result, getDate[1]


# ==========1225
# 持續檢查欄位是否有相近日期
# 再由日期對應課號找到userid
def check_date_in_sheet():
    # 檢查試算表中的日期欄位
    # 透過 Google Sheets API 讀取特定範圍的日期欄位，這裡以 A1:D3 為例
    range_name = "A1:D3"  # 替換為您的欄位範圍
    values = sheet.get(range_name)

    # 檢查日期欄位是否包含今天日期的資料
    for row in values:
        for cell in row:
            if today in cell:
                # 如果有匹配的日期，這裡可以執行相應的任務或操作
                # 例如通知使用者或進行其他處理
                print(f"日期 {today} 匹配到在試算表中的 {cell} 欄位")
                # 在這裡執行您希望觸發的任務或操作


# print(type(str(getCourseNum("U40312c953c499d83cb749fc62140c42e"))))
# getCourses("C01-1")
# print(noticeTeacher("12/26"))
