import pygsheets
import pandas as pd
import schedule
import time
from datetime import datetime, timedelta


auth_file = "flybot.json"
gc = pygsheets.authorize(service_file=auth_file)
sheet_id = "1KYsTpbF6eiTT3-GP3VFlXdiOWe8WwCa5z6ZA1XC1RKk"
sh = gc.open_by_key(sheet_id)


wks = sh.worksheet_by_title("course")
wks2 = sh.worksheet_by_title("teacher")


def setCourse(name, user):
    # If multiple numbers are provided, split them and update the worksheet for each number
    # num_list = num.split(",")

    # for n in num_list:
    row = (
        len(wks2.get_col(1, returnas="cell", include_empty=False)) + 1
    )  # Find the next available row
    #     n = n.strip()
    wks2.update_values(f"A{row}", [[name]])  # Add the data to the next avai
    wks2.update_values(f"B{row}", [[user]])

    # n = n.split(" ")
    # wks2.update_values(f"C{row}", [[n[1]]])


def getDeatilByUser(id):
    results = wks2.find(id)
    dt = ""
    if results:
        courseList = []
        for i in results:
            r = int(i.row)
            name = wks2.get_value(f"A{r}")
            # print(name)
            target = wks.find(name)
            for t in target:
                r = t.row
                dt = wks.get_value(f"A{r}") + " " + wks.get_value(f"B{r}")
                courseList.append(dt)
            courseList = "\n".join(courseList)
        return courseList  # ['Speaking Part 1 & 2 01/03(三)', 'Speaking Part 2 & 3 01/05(三)']

    else:
        return False


# def getUser(re):
#     for r in re:
#         target = wks.find(r)
#         for t in target:
#             r = int(t.row)
#             userName = wks.get_value(f"B{r}")
#             if wks2.find(userName):
#                 id = wks2.find(userName)
#                 for i in id:
#                     r = int(i.row)
#                     userID = wks2.get_value(f"B{r}")
#                     return userID
#             else:
#                 return "not found in teacher"
def getUser(re):
    target = wks.find(re)
    for t in target:
        r = int(t.row)
        userName = wks.get_value(f"C{r}")
        if wks2.find(userName):
            id = wks2.find(userName)
            for i in id:
                r = int(i.row)
                userID = wks2.get_value(f"B{r}")
                return userID
        else:
            return "not found in teacher"


# print(getUser("id"))


def delUser(id):
    results = wks2.find(id)
    if results:
        for i in results:
            r = int(i.row)

            wks2.delete_rows(r, 1)  # 起始,結束
        print("刪除成功")
    else:
        print("刪除失敗")


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


def check_date_in_sheet():
    # 檢查試算表中的日期欄位
    try:
        # all_values = wks2.get_all_values()
        # delExpireRow()
        next_day = get_next_day(getToday())
        # print(today, next_day)
        target = wks.find(next_day)
        # print(f'在{target}')
        re = []
        if target:
            for t in target:
                r = t.row

                re.append(wks.get_value(f"A{r}"))

        else:
            print("今天無")

        return re
    except Exception:
        return 0


def delExpireRow():
    expireDate = getToday()
    expireTarget = wks.find(expireDate)
    if expireTarget:
        rows = []
        # print(expireTarget)
        for t in expireTarget:
            r = int(t.row)
            # print(r)
            wks.update_values(f"A{r}", [[""]])
            wks.update_values(f"B{r}", [[""]])
            wks.update_values(f"C{r}", [[""]])

        # print(getToday())
        # print("刪除過期成功")
    else:
        return 0


def getDateFromCourse(course):
    for c in wks.find(course):
        row = int(c.row)
        date = wks.get_value(f"B{row}")
        return date


def isExist(id):
    if wks2.find(id):
        return True
    else:
        return False
