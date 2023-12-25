import pygsheets
import pandas as pd


def setCourse(num, user):
    try:
        # authorization
        gc = pygsheets.authorize(
            service_file="D:/SideProject/flight/flyline/flybot.json"
        )
        # open the google spreadsheet
        sh = gc.open_by_key("1KYsTpbF6eiTT3-GP3VFlXdiOWe8WwCa5z6ZA1XC1RKk")

        # select the first worksheet
        wks = sh.worksheet_by_title("teacher")
        df = pd.DataFrame(wks.get_all_records())
        wks.set_dataframe(df, "A1")  # 從欄位 A1 開始
        c = " "
        if c in num:
            listnum = num.split(" ")
            for i in listnum:
                row = (
                    len(wks.get_col(1, returnas="cell", include_empty=False)) + 1
                )  # Find the next available row
                wks.update_value(f"A{row}", i)  # Add the data to the next avai
                wks.update_value(f"B{row}", user)

        else:
            row = (
                len(wks.get_col(1, returnas="cell", include_empty=False)) + 1
            )  # Find the next available row
            wks.update_value(f"A{row}", num)  # Add the data to the next avai
            wks.update_value(f"B{row}", user)
    except Exception:
        return False
