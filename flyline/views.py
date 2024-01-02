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
    ConfirmTemplate,
    PostbackEvent,
    PostbackAction,
    PostbackTemplateAction,
)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


def notice(Userid, detail):
    emoji = [
        {"index": 7, "productId": "5ac21a13031a6752fb806d57", "emojiId": "142"},
    ]

    # print(detail)
    if detail:
        t = f"您有課程在明天$\n{detail}"
        line_bot_api.push_message(
            Userid,
            TextSendMessage(
                text=t,
                emojis=emoji,
            ),
        )


def check_spreadsheet():
    try:
        numAndDate = check_date_in_sheet()  # 檢查今天是否有需要通知的日期
    # print(numAndDate)
        if numAndDate:  # 如果有
            # print(numAndDate)
            user = getUser(numAndDate)
            for detail, id in zip(numAndDate, user):
                notice(id, detail)  # 通知
                print(f"通知{id}成功")
        else:
            print("not find")
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
                        TextSendMessage(
                            text="輸入暱稱：XX老師/教官"
                        ),
                    )
                elif event.postback.data == "學生":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="目前不開放學生綁定"),
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
                    if (isExist(uid) != True):
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
                                            label="我是老師", text="我是teacher", data="teacher"
                                        ),
                                    ],
                                ),
                            ),
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token, TextSendMessage(text="資料已存在")
                        )
                elif("老師" in rcMsg) or ("教官" in rcMsg) or ("助教" in rcMsg ) or ("教室" in rcMsg):
                    
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
scheduler.add_job(check_spreadsheet, "interval", seconds=60)
# scheduler.add_job(check_spreadsheet, "cron", hour="17,20")  # 設定每天的下午3點及晚上7點（24小時制）
scheduler.start()
# ===============
# 先綁定再做
# ================


# 部屬後設定，每日12, 18執行doChecking更新
