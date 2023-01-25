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
ACCESS_TOKEN = "F77aAQiczRnjFDAoaahcP352HXsf3mI92O+1zpHpFe+P/1jbZiN34DGpx62GZDYxeJ/aMNIF8BxVSm70tktkiI82Agjfqs+u3BiHLagq7QqNv0yD9WYa03VA01H2wqg781vtdSt2ibxbfxzBLTc5yQdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler('3c0352a060105077c4266862efa1e4a6')

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
    senderId = event.source.user_id
    msg = event.message
    img_id = msg.id
    content = line_bot_api.get_message_content(img_id)
    pred = model.predict(content.content)
    name = pred[0]
    index = pred[1]
    classes = pred[2]
    response = """พบว่าเป็นโรค {} ({}%)""".format(name,round(float(classes[index]),4)*100)

    if name == 'tungro' :
      response +="\n วิธีการรักษา"
    elif name == 'ustilaginoidea' :
      response +="\n วิธีการรักษา"
    elif name == 'bipolaris' :
      response +="\n วิธีการรักษา"
    else :
      response +="\n วิธีการรักษา"
      
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))



if __name__ == "__main__":
    app.run(debug=True,port=8888)