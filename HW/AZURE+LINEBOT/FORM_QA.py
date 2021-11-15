# 載入相關套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, AudioSendMessage
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime
import json
import mysql.connector
import MySQLdb
import os
import re
import http.client, json

if not os.path.exists('./images'):
    os.mkdir("./images")

# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi(
    '0mqiSE/VDhcb56P3B5bVo1UrsoW3kmDwjinNMGQ6NNZqMAXjcJ2XpoX+a7GYLLViIFRepOsopCuJaYIQJM+WWt36n++92aBiAKVyGQb6Gy36JLUTAO2iqhvpQMjX99MPvugpalLfG2q6ODzLy8k6hQdB04t89/1O/w1cDnyilFU=')
# your linebot message API - Channel secret
handler = WebhookHandler('9d06d17c8cfaf212ed1eca5a5fa3e990')


# linebot接收訊息
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


host = 'testtest12322.azurewebsites.net'  # 主機
endpoint_key = "0d45c53d-1054-4798-820a-1bea848e3c3c"  # 授權碼
kb = "5758b025-bb88-4178-9a4a-35253a065872"  # GUID碼
method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"


@handler.add(MessageEvent, message=TextMessage)
def handel_messafe(event):
    mtext = event.message.text
    if mtext == '@藥物資訊':
        sendUse(event)

    else:
        sendQnA(event, mtext)


def sendUse(event):  # 藥物資訊
    try:
        text1 = """請輸入藥物健保代碼:
        """

        message = TextSendMessage(
            text=text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendQnA(event, mtext):  # QA
    question = {
        'question': mtext,
    }
    content = json.dumps(question)
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }
    conn = http.client.HTTPSConnection(host)
    conn.request("POST", method, content, headers)
    response = conn.getresponse()
    result = json.loads(response.read())
    result1 = result['answers'][0]['answer']
    if 'No good match' in result1:
        text1 = '很抱歉，請輸入正確藥物健保代碼:。'
    else:
        result2 = result1[2:]  # 移除「A：」
        text1 = result2
    message = TextSendMessage(
        text=text1
    )
    line_bot_api.reply_message(event.reply_token, message)




# linebot處理照片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 使用者傳送的照片
    message_content = line_bot_api.get_message_content(event.message.id)

    # 照片儲存名稱
    fileName = event.message.id

    # 儲存照片
    with open('./images/{}'.format(fileName) + '.jpg', 'wb')as f:
        for chunk in message_content.iter_content():
            f.write(chunk)



    endpoint = "https://testform1111.cognitiveservices.azure.com/"
    credential = AzureKeyCredential("3254d83e14b44f44bc4abad90a169771")

    form_recognizer_client = FormRecognizerClient(endpoint, credential)

    with open(f"./images/{fileName}.jpg", "rb") as fd:
        form = fd.read()

    poller = form_recognizer_client.begin_recognize_content(form)
    form_pages = poller.result()

    datas = []
    for content in form_pages:
        for table in content.tables:
            for cell in table.cells:
                datas.append(cell.text)


    # 去除影像辨識錯誤，最後面欄位的空白
    n = len(datas) % 7
    if n != 0:
        del datas[-n:]

    # 大寫字母O ---> 數字0
    for i in range(len(datas)):
        if len(datas[i]) == 10:
            datas[i] = datas[i].replace('O', '0')

    regex = re.compile(r'[A-Z]{2}\d{6}[G,\d]\d')
    drugId = str(list(filter(regex.match, datas)))



    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='藥物健保代碼: '+ drugId))


# 開始運作Flask
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12345)