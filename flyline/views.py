from flyline.t2 import *
from threading import Thread
import time
from apscheduler.schedulers.background import BackgroundScheduler

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
    MessageAction,
    ConfirmTemplate,
    PostbackEvent,
    PostbackAction,
    PostbackTemplateAction,
)

line_bot_api = LineBotApi(
    "oPfO16vQOYT+7nHYUmUZ67tQX4FpNmEzbnd6lnLBDscB1PQ22c8Vnei2DCRIf94EhJtyFzRUjGWJ4wdikOiD+uxJ8QlULl/76r/er4XY1sUepPLLsVYmm074L/ZZx2yDtNedL6WFi5Eo8ljhVoq/jgdB04t89/1O/w1cDnyilFU="
)
parser = WebhookParser("88c24b64b2af3ea8b6597232821c24e5")


def notice(Userid, detail):
    line_bot_api.push_message(
        Userid,
        TemplateSendMessage(
            alt_text="到課提醒",
            template=ButtonsTemplate(
                title="確認出席明日課程",
                text=f"{detail}",
                actions=[PostbackAction(label="我會準時到", text="我會準時到", data="準時")],
            ),
        ),
    )


def check_spreadsheet():
    try:
        numAndDate = check_date_in_sheet()
        if numAndDate:
            for d in numAndDate:
                user = getUser(d)
                notice(user, d)
        time.sleep(10)

    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        time.sleep(10)


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
            uid = event.source.user_id  # 取user id

            if isinstance(event, PostbackEvent):  # 如果有postback事件
                if event.postback.data == "teacher":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="(同課表上名稱) 輸入名稱："),
                    )
                elif event.postback.data == "學生":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="目前不開放學生綁定"),
                    )
                if event.postback.data == "準時":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="感謝您的回覆"),
                    )
                if event.postback.data == "刪除":
                    delUser(event.source.user_id)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="刪除成功"),
                    )
            elif isinstance(event, MessageEvent):
                rcMsg = event.message.text
                if rcMsg == "綁定":
                    if isExist(uid) != True:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="Buttons template",
                                template=ButtonsTemplate(
                                    title="身分選擇",
                                    text="請選擇綁定身分",
                                    actions=[
                                        PostbackTemplateAction(
                                            label="我是學生", text="我是student", data="學生"
                                        ),
                                        PostbackTemplateAction(
                                            label="我是老師",
                                            text="我是老師",
                                            data="teacher",
                                        ),
                                    ],
                                ),
                            ),
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token, TextSendMessage(text="資料已存在")
                        )
                elif "@" in rcMsg:
                    rcMsg = rcMsg[1:]
                    setCourse(rcMsg, uid)  # 不存在則寫入
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="綁定成功"),
                    )

                elif rcMsg == "解除綁定":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text="Confirm template",
                            template=ConfirmTemplate(
                                text="您確定要解除綁定?(會一併刪除所有紀錄)",
                                actions=[
                                    PostbackAction(label="是", text="是", data="刪除"),
                                    PostbackTemplateAction(
                                        label="否", text="否", data="不刪除"
                                    ),
                                ],
                            ),
                        ),
                    )

                elif rcMsg == "查詢(查詢需等待)":
                    detail = getDeatilByUser(uid)
                    if detail:  # 如果這個人的資料存在
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="本月課程有:\n" + detail),
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="無您的資料，請重新綁定通知"),
                        )
                elif event.message.type == "sticker":
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="收到你的貼圖囉！")
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


scheduler = BackgroundScheduler()
# scheduler.add_job(check_spreadsheet, "interval", seconds=10)
scheduler.add_job(check_spreadsheet, "cron", hour="18")  # 設定前一天的晚上6點（24小時制）
# scheduler.add_job(check_spreadsheet, "interval", seconds=30)  # 設定每天的下午3點及晚上7點（24小時制）

scheduler.start()
# ===============
# 先綁定再做
# ================


# 部屬後設定，每日12, 18執行doChecking更新
