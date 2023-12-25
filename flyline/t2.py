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


def getCourseNum(item):
    try:
        nums = wks2.find(item)  # 找userId位置
        for i in nums:
            r = int(i.row)
            c = int(i.col)
            item = wks2.get_values(start=(r, c + 1), end=(r, c + 1))[0][0]
            return item  # 取出userid
    except Exception:
        return False


# 綁定後 從userid找課號
# 先取出此刻號有幾堂課and日期，再做
# 再tour李find tcinfo，取出日期
def getTargetDetail(item):
    results = wks.find(item)
    results = results[0].value.split(",")  # 找到包含課號的第一個，再以","分割
    # print(results)
    for result in results:
        # print(result.strip())
        result = result.strip()
        # 一列以空格區分([0]課號[1]日期[2]時間) => C01-1 12/29(五) 19:00-22:00數學
        return result


# ==========1225
# 持續檢查欄位是否有相近日期
# 再由日期對應課號找到userid
def check_date_in_sheet():
    # 檢查試算表中的日期欄位
    # 透過 Google Sheets API 讀取特定範圍的日期欄位，這裡以 A1:D3 為例
    all_values = wks.get_all_values()

    # Regular expression pattern to find course numbers and associated dates
    pattern = re.compile(r"\b[A-Za-z]\w*-\d+")
    date_pattern = re.compile(r"\b\d{1,2}/\d{1,2}")

    # Dictionary to store course numbers and associated dates
    courses_with_dates = {}

    # Collect course numbers and associated dates
    for row in all_values:
        for cell in row:
            course_matches = pattern.findall(cell)
            date_matches = date_pattern.findall(cell)
            for course, date in zip(course_matches, date_matches):
                courses_with_dates[course] = date
    today = datetime.date.today()
    next_day = today + datetime.timedelta(days=1)
    formatted_next_day = next_day.strftime("%m/%d")
    # Display course numbers with associated dates
    for course, date in courses_with_dates.items():
        if formatted_next_day == date:
            # print(f"{date}有課程{course}")
            return course, date


print(getTargetDetail(check_date_in_sheet()[0]))
# getCourses("C01-1")
# print(noticeTeacher("12/26"))
