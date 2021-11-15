# 載入相關套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime
import re
import pandas as pd

# create flask server
app = Flask(__name__)
# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = LineBotApi('T9vMMKzQTDhvdsFJWFDtjVKcI56KL0bx3cyKOTN8jN3AWG4lrzMRP1C3Sc69c+a08iHOeqHDkMOvDOSyqD5+zwCdqdSSHTDSBz2WGJ3nezkX5lLZ6A23tgNlwLRHl/X5mQaSt0UBvSPHJpFmp9hHiAdB04t89/1O/w1cDnyilFU=')
# your linebot message API - Channel secret
handler = WebhookHandler('9bfda1bf917044c86fe056c26660e234')


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

# linebot處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # linebot回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='收到您的訊息囉!'))


# linebot處理照片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 使用者傳送的照片
    message_content = line_bot_api.get_message_content(event.message.id)

    # 照片儲存名稱
    fileName = event.message.id + '.jpg'

    # 儲存照片
    with open('./' + fileName, 'wb')as f:
        for chunk in message_content.iter_content():
            f.write(chunk)
    
    # Azure Form Recognizer
    endpoint = "https://formfong.cognitiveservices.azure.com/"
    credential = AzureKeyCredential("61e429884959460abc7c4955f3a108be")

    form_recognizer_client = FormRecognizerClient(endpoint, credential)
    
    # 讀取圖片
    local_image = open('./' + fileName, 'rb')

    poller = form_recognizer_client.begin_recognize_content(local_image)
    form_pages = poller.result()

    datas = []
    for content in form_pages:
        for table in content.tables:
            for cell in table.cells:
                datas.append(cell.text)
   
    # 大寫字母O ---> 數字0
    for i in range(len(datas)):
        if len(datas[i]) == 10:
            datas[i] = datas[i].replace('O', '0')

    regex = re.compile(r'[A-Z,\d]{2}\d{6}[G,\d]\d')
    med_no = list(filter(regex.match, datas))
    
    result = ''
    for drug in med_no:
        A = [drug]
        df = pd.read_csv("notices.csv")
        df_med = df[df["健保代碼"].isin(A)]
        for (colname,colval) in df_med.iteritems():
            content = str('%s: %s,'%(colname, colval.values)) + '\n'
            result += content
        
    # linebot測試回傳健保代碼   
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result))
    
# 開始運作Flask
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12345)