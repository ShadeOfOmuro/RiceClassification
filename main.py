from flask import Flask, request, abort
import PIL.Image as Image
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage , ImageMessage
import io
from fastai import * 
from fastai.vision.all import *

app = Flask(__name__)
print("loading model")
model = load_learner("bestFull.pth",cpu=True)
ACCESS_TOKEN = "<YOUR_ACCESS_TOKEN>"
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler('<YOUR_CHANNAL_SECRET>')

@app.route("/")
def home():
  return "I'm alive"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    msg = event.message
    img_id = msg.id
    content = line_bot_api.get_message_content(img_id)
    pred = model.predict(content.content)
    name = pred[0]
    index = pred[1]
    classes = pred[2]
    response = """พบว่าเป็นโรค {} ({}%)""".format(name,round(float(classes[index]),2))
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    if name == 'โรค1' :
      response = """พบว่าเป็นโรค {} ({}%)""".format(name,round(float(classes[index]),2))
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    elif name == 'โรค2' :
      response = """พบว่าเป็นโรค {} ({}%)""".format(name,round(float(classes[index]),2))
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    elif name == 'โรค3' :
      response = """พบว่าเป็นโรค {} ({}%)""".format(name,round(float(classes[index]),2))
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    else :
      response = """พบว่าเป็นโรค {} ({}%)""".format(name,round(float(classes[index]),2))
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))



if __name__ == "__main__":
    app.run(debug=True,port=8888)