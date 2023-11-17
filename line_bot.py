from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (TextSendMessage, ImageSendMessage)
import datetime

def reply_to_line(line_event, reply_message):
    print(str(datetime.datetime.now()) + " INFO: Sedning reply to LINE")
    line_bot_api.reply_message(
        line_event.reply_token,
        TextSendMessage(text=reply_message),
    )

def reply_with_image_to_line(line_event, image_url):
    print(str(datetime.datetime.now()) + " INFO: Sending image reply to LINE")
    line_bot_api.reply_message(
        line_event.reply_token,
        ImageSendMessage(original_content_url=image_url, preview_image_url=image_url),
    )