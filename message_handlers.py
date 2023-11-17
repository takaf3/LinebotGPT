from linebot.models import (MessageEvent, TextMessage, StickerMessage, ImageMessage)
from openai_chat import classify_user_input, query_openai_chat, query_openai_vision, query_openai_dalle
from line_bot import reply_to_line, reply_with_image_to_line
import base64
from io import BytesIO
import datetime

assist_message = ""
image_data = None

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text
    global assist_message
    global image_data

    isDalle = classify_user_input(user_message)

    if image_data is not None:
        reply = query_openai_vision(user_message, image_data)
        image_data = None  # Clear the image data after using it
    else:
        if isDalle == "NO":
            print(str(datetime.datetime.now()) + " DALLE?: " + "NO")
            reply = query_openai_chat(assist_message, user_message)
        elif isDalle == "YES":
            print(str(datetime.datetime.now()) + " DALLE?: " + "YES")
            result = query_openai_dalle(user_message)
            image = result.data[0].url
            reply = result.data[0].revised_prompt
        else:
            print(str(datetime.datetime.now()) + " DALLE?: " + "EROOR")
            isDalle = "NO"
            reply = "ん、ごめんもう一回言って！"

    assist_message = reply

    if isDalle == "NO":
        reply_to_line(event, reply)
    else:
        reply_with_image_to_line(event, image)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    if event.message.keywords is not None:
        global assist_message
        keywords = "".join(event.message.keywords)
        user_message = "Please try replying in Japanese. I sent a sticker that has keywords of: " + keywords
        reply = query_openai_chat(assist_message, user_message)
        assist_message = reply
    else:
        reply = "スタンプ！"

    reply_to_line(event, reply)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    global image_data

    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    image_bytes = BytesIO()
    for chunk in message_content.iter_content():
        image_bytes.write(chunk)

    image_bytes.seek(0)
    image_data = base64.b64encode(image_bytes.read()).decode('utf-8')

    reply = "画像きた！なんでもきいて！"
    assist_message = reply
    reply_to_line(event, reply)