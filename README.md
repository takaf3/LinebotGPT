# README.md

This is a Python script that uses Flask, LINE Messaging API, and OpenAI API to create a chatbot that can respond to text, sticker, and image messages.

## Dependencies

- Flask
- linebot
- openai

## Environment Variables

- LINE_CH_ACCESS_TOKEN: Your LINE Channel access token.
- LINE_CH_SECRET: Your LINE Channel secret.
- OPENAI_API_KEY: Your OpenAI API key.

## How to Run

1. Set your environment variables.
2. Run the script with `python main.py`.

## How it Works

When a message event (text, sticker, or image) is received from LINE, the script will process the message and generate a response using OpenAI's GPT-4 model. The response is then sent back to the user through LINE.

For text messages, the script simply sends the user's message to OpenAI and returns the generated response.

For sticker messages, if the sticker has keywords, the script sends a message to OpenAI that includes the keywords. If the sticker does not have keywords, the script sends a default response.

For image messages, the script first encodes the image into base64 format, then sends a message to OpenAI that includes the encoded image. The script then returns the generated response.

The script also logs some information, such as when it sends a reply to LINE or when it sends a message to OpenAI.
