from django.shortcuts import render
from flyline.t import *
from flyline.t2 import *

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    QuickReply,
    QuickReplyButton,
    MessageTemplateAction,
    PostbackEvent,
    PostbackAction,
    PostbackTemplateAction,
)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, PostbackEvent):  # 如果有回傳值事件
                if event.postback.data == "老師":
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="請輸入課號:(多個請以空格區分 至多3個)")
                    )

            elif isinstance(event, MessageEvent):
                rcMsg = event.message.text
                if "-" in rcMsg:
                    try:
                        courseNum = event.message.text
                        uid = event.source.user_id  # 取user id

                        setCourse(courseNum, uid)
                        if setCourse:
                            line_bot_api.reply_message(
                                event.reply_token, TextSendMessage(text="綁定成功")
                            )

                    except Exception:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="綁定失敗請再輸入一次，格式需完整填寫"),
                        )
                elif rcMsg == "綁定":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text="Buttons template",
                            template=ButtonsTemplate(
                                title="身分選擇",
                                text="請選擇綁定身分",
                                actions=[
                                    PostbackTemplateAction(
                                        label="我是學生", text="我是學生", data="學生"
                                    ),
                                    PostbackTemplateAction(
                                        label="我是老師", text="我是老師", data="老師"
                                    ),
                                ],
                            ),
                        ),
                    )
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="很抱歉，我們不能處理這則訊息")
                )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# def noticeTeacher(date,uid):
#     match = re.search(r"(\d{1,2})/(\d{1,2})", date)
#     if match:
#         month = int(match.group(1))
#         day = int(match.group(2))
#         year = datetime.datetime.now().year  # 取得當前年份
#         extracted_date = datetime.date(year, month, day)
#         today = datetime.date.today().strftime("%m/%d")  # 獲取當前日期，格式為 MM/DD
#         rdate = extracted_date.strftime("%m/%d")  # 表單上的日期
#         target_date = extracted_date - datetime.timedelta(days=1)
#         schedule_date = target_date.strftime("%m/%d")  # 表單上的日期的前一天(目標日)
#         # print(schedule_date)
#         if today == schedule_date:
#             notice(uid)
#             return target_date
#         # print(f"日期 {schedule_date} 是今天目標日，表單上 {rdate} 欄位，{target_date}")
#     else:
#         return None  # 如果未找到匹配的日期格式，返回 None 或者其他您認為適合的值


def notice(Userid):
    emoji = [
        {"index": 7, "productId": "5ac21a13031a6752fb806d57", "emojiId": "142"},
    ]

    detail = getTargetDetail(check_date_in_sheet())
    # print(detail)
    if detail:
        t = f"您有課程在明天${detail}"
        line_bot_api.push_message(
            Userid,
            TextSendMessage(
                text=t,
                emojis=emoji,
            ),
        )


# ===============
# 先綁定再做
# ================

import time


def doChecking():
    while True:
        item = check_date_in_sheet()
        if item:
            userid = getCourseNum(item[0])
            notice(userid)
        else:
            time.sleep(60)  # 休息 60 秒後再次檢查
            continue  # 繼續執行下一次的 doChecking()


doChecking()
