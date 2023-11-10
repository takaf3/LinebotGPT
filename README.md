# LinebotGPT

This is a Python script that uses Flask, LINE Messaging API, and OpenAI API to create a chatbot that can respond to text, sticker, and image messages.

## Dependencies

- Python 3.9 or later
- Flask
- linebot
- openai

## Environment Variables

- LINE_CH_ACCESS_TOKEN: Your LINE Channel access token.
- LINE_CH_SECRET: Your LINE Channel secret.
- OPENAI_API_KEY: Your OpenAI API key.

## How to Run
1. Install the required Python packages by running `pip install -r requirements.txt`.
2. Create a LINE Messaging API channel. You can follow the instructions provided [here](https://developers.line.biz/en/docs/messaging-api/getting-started/).
3. Obtain the Channel Access Token and Channel Secret from the LINE Developers console and set them as environment variables.
4. Obtain the OpenAI API key from the OpenAI website and set it as an environment variable.
5. Run the `main.py` with `flask run`.
6. Set your server URL to the webhook URL for your LINE Messaging API channel on LINE Developers console.

## How it Works

When a message event (text, sticker, or image) is received from LINE, the script will process the message and generate a response using OpenAI's GPT-4 model. The response is then sent back to the user through LINE.

For text messages, the script simply sends the user's message to OpenAI and returns the generated response.

For sticker messages, if the sticker has keywords, the script sends a message to OpenAI that includes the keywords. If the sticker does not have keywords, the script sends a default response.

For image messages, the script first encodes the image into base64 format. It then waits for a subsequent user message. Both the encoded image and the user message are sent together to OpenAI's Vision API. The script then returns the generated response.

The script also logs some information, such as when it sends a reply to LINE or when it sends a message to OpenAI.
