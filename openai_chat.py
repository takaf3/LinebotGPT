from openai import OpenAI
import datetime

def classify_user_input(user_message):
    print(str(datetime.datetime.now()) + " INFO: Classifing user input with gpt3.5-turbo...")
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful analyst who are specialized in telling if the user wants an image generated or not given the user input. Please reply 'YES' or 'NO' and nothing else. You should not reply 'YES' unless you are absolutely confident. For example, only a word input should not mean the user wanting an image to be generated."},
            {"role": "user", "content": user_message},
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
    print(str(datetime.datetime.now()) + " INFO: Sending request to OpenAI DALLE...")
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=user_message,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response