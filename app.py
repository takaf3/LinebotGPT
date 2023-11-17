from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, StickerMessage, ImageMessage)
import os
from openai import OpenAI
from line_bot import reply_to_line, reply_with_image_to_line
from message_handlers import handle_text_message, handle_sticker_message, handle_image_message

app = Flask(__name__)

if "LINE_CH_ACCESS_TOKEN" in os.environ and "LINE_CH_SECRET" in os.environ and "OPENAI_API_KEY" in os.environ:
    line_bot_api = LineBotApi(os.environ["LINE_CH_ACCESS_TOKEN"])
    handler = WebhookHandler(os.environ["LINE_CH_SECRET"])
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
else:
    print("Required environment variables not set. Exiting...")
    exit(1)

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
        print(str(datetime.datetime.now()) + " INFO: Signature valid")
    except InvalidSignatureError:
        print("ERROR: Signature Invalid. Check your channell access token.")
        abort(400)
    return 'OK'

if __name__ == '__main__':
    app.run()