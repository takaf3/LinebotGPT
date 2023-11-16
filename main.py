import base64
import datetime
import os
from io import BytesIO

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, StickerMessage, ImageMessage, TextSendMessage, ImageSendMessage)

from openai import OpenAI

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_CH_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CH_SECRET"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

assist_message = ""
image_data = None

def reply_to_line(line_event, reply_message):
    print(str(datetime.datetime.now()) + " INFO: Sedning reply to LINE")
    line_bot_api.reply_message(
        line_event.reply_token,
        TextSendMessage(text=reply_message),
    )

def classify_user_input(user_message):
    print(str(datetime.datetime.now()) + " INFO: Sending message to OpenAI Text...")
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful analyst who can analyze the user input and tell wether if the user wants an image or not as a reply from chatbot. Reply YES or NO based on the analysis. Do not reply anything else."},
            {"role": "user", "content": "This is the user input: " + user_message},
        ]
    )
    return response.choices[0].message.content    

def query_openai_chat(assist_message, user_message):
    print(str(datetime.datetime.now()) + " INFO: Sending message to OpenAI Text...")
    response = openai_client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a friend of this user. They want to have a chat with you like a friend. Your reply should not be long, should be like a text message reply. Try not to use so many emojis. Be friendly and reply like so. You are using a message app called LINE which is the standard in Japan."},
            {"role": "assistant", "content": assist_message},
            {"role": "user", "content": user_message},
        ]
    )
    return response.choices[0].message.content

def query_openai_vision(message, encoded_image):
    print(str(datetime.datetime.now()) + " INFO: Sending message to OpenAI Vision...")
    response = openai_client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a friend of this user. They want to have a chat with you like a friend. Your reply should not be long, should be like a text message reply. Try not to use so many emojis. Be friendly and reply like so. You are using a message app called LINE which is the standard in Japan."},
            {"role": "user", "content": [
                    {"type": "text", "text": message},
                    {"type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}",},
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

def query_openai_dalle(user_message):
    print(str(datetime.datetime.now()) + " INFO: Sending message to OpenAI DALLE...")
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=user_message,
        size="512x512",
        quality="standard",
        n=1,
    )

    return response.data[0].url

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

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text
    global assist_message
    global image_data

    if image_data is not None:
        reply = query_openai_vision(user_message, image_data)
        image_data = None  # Clear the image data after using it
    else:
        if classify_user_input(user_message) == "NO":
            print(str(datetime.datetime.now()) + " DALLE?: " + "NO")
            reply = query_openai_chat(assist_message, user_message)
        elif classify_user_input(user_message) == "YES":
            print(str(datetime.datetime.now()) + " DALLE?: " + "YES")
            reply = query_openai_dalle(user_message)
        else:
            print(str(datetime.datetime.now()) + " DALLE?: " + "EROOR")
            reply = "ん、ごめんもう一回言って！"

    assist_message = reply

    reply_to_line(event, reply)

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


if __name__ == '__main__':
    app.run()