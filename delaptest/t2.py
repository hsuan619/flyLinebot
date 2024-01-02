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
    if(results):
        courseList = []
        for i in results:
            r = int(i.row)
            c = int(i.col)
            name = wks2.get_values(start=(r, c - 1), end=(r, c - 1))[0][0]
        detail = wks.find(name)
        for n in detail:
            rn = int(n.row)
            dt = wks.get_value(f"A{rn}")
            
            courseList.append(dt)
        courseList = '\n'.join(courseList)
        return courseList #['Speaking Part 1 & 2 01/03(三)', 'Speaking Part 2 & 3 01/05(三)']
    else:
        return False


def getUser(re):
    name = []
    idList = []
    for r in re:
        target_detail = wks.find(r)
        
        if(target_detail):
            for t in target_detail:
                r = t.row
                n = wks.get_value(f"B{r}") #name
                name.append(n)
    for id in name:
        target_id = wks2.find(id)
        for td in target_id:
            r = td.row
            id = wks2.get_value(f"B{r}") #name
            idList.append(id)
    return idList



def userName(course):
    target_detail = wks.find(course)
    if(target_detail):
        for t in target_detail:
            r = t.row
            n = wks.get_value(f"B{r}") #name
            return n    
            
def getUserID(name):
    target_id = wks2.find(name)
    if(target_id):
        for t in target_id:
            r = t.row
            n = wks2.get_value(f"B{r}") #name
            return n
def delUser(id):
    rows = []
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
                re.append(t.value)

        else:
            print("今天無")
        
        return re
    except Exception:
        return 0

def getDetailByDate(reList):  # 從課表抓詳細課程.
    
    resultList = ""
    for r in reList:
        
        results = wks.find(r)
        
        # print(results)
        if results:
            # print(results[0].value)
            resultList = (results[0].value) + "\n" + resultList
            resultList = resultList.strip()

        else:
            return "沒有符合"
    return resultList


# def delExpireRow():
#     expireDate = get_pre_day(getToday())
#     expireTarget = wks.find(expireDate)
#     if expireTarget:
#         rows = []
#         # print(expireTarget)
#         for t in expireTarget:
#             r = int(t.row)
#             print(r)
#             wks.delete_rows(r,1)
            
#         return 1
#         # print(getToday())
#         # print("刪除過期成功")
#     else:
#         return 0
def isExist(id):
    if(wks2.find(id)):
        return True
    else:
        return False
