from django.shortcuts import render
from flyline.t import *

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
    MessageTemplateAction,
    PostbackEvent,
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
            if isinstance(event, MessageEvent):
                rcMsg = event.message.text
                msg = []
                if rcMsg == "綁定":
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
                # elif "c" in event.message.text or "C" in event.message.text:
                #     profile = event[0].source.userId
                #     course = event.message.text
                #     getCourse(course, profile)
                #     if getCourse:
                #         msg.append(TextSendMessage(text="綁定成功！"))
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
                if event.postback.data == "老師":
                    uid = event.source.user_id
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=uid)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
