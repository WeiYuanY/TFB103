from flask import Flask
from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, QuickReply, QuickReplyButton, MessageAction
import pymysql
import re
import os
import pandas as pd
import rec_func



#健保卡
if not os.path.exists('./images/healthIDcard'):
    os.mkdir("./images/healthIDcard")

#處方箋
if not os.path.exists('./images/prescriptionNote'):
    os.mkdir("./images/prescriptionNote")

#讀取藥物交互作用檔
df = pd.read_csv("NIHdrugbankall.csv",sep="\t",encoding='latin1')
ref = pd.read_csv("all.csv")
ref.drop_duplicates(subset = ['inter_type'], keep = 'first',inplace = True)

#判斷輸入的是電話號麻
Telephoneno = ['02', '03', '037', '04', '049', '05', '06', '07', '08', '089', '082', '0826', '0836']

#宣告app 物件
app = Flask(__name__)

#Line bot
line_bot_api = LineBotApi('Channel secret')
handler = WebhookHandler('Channel access token')


#基本設定
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#收到照片
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # get user info & message
    LineID = event.source.user_id
    LineName = line_bot_api.get_profile(LineID).display_name
    userInfo = LineID + LineName

    # get msg details
    print('msg from [', userInfo, ']')

    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='請先點擊【處方箋辨識】的功能圖示，再重新上傳照片，謝謝!'))

#收到文字
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user info & message
    LineID = event.source.user_id
    LineName = line_bot_api.get_profile(LineID).display_name
    userInfo = LineID + LineName
    msg = event.message.text

    # get msg details
    print('msg from [', userInfo, '] : ', msg)

    if msg == "加入會員":
        joinUs(event)

    elif msg == '手機':
        cellphone(event)

    elif msg == '手機號碼':
        cellphoneNo(event)

    #判斷使用者輸入的是手機號碼
    elif msg[0:1] == '09':
        inserCellPhoneNo(event)

    elif msg == '電話':
        telephone(event)

    elif msg == '電話號碼':
        telephoneNo(event)

    #判斷使用者輸入的是電話號碼
    elif msg[0:2] in Telephoneno:
        inserTellPhoneNo(event)

    elif msg == '個人用藥查詢':
        personal(event)

    elif msg == '其他會員服務':
        otherService(event)

    elif msg == '個人資料':
        personalInfo(event)

    elif msg == '查詢個人資料':
        personalInfoSearsh(event)

    elif msg == '修改個人資料':
        personalInfoupdate(event)

    elif msg == '上傳處方箋':
        rxForm(event)

    elif msg == '藥物交互作用查詢':
        drugInteractions(event)

    elif msg == '好食推薦':
        greatFood(event)

    elif msg == '推薦食材':
        recommendedFood(event)

    elif msg == '回診醫院':
        hospitalReserve(event)

    elif msg == '早餐表格':
        breakfast(event)

    elif msg == '午餐表格':
        lunch(event)

    elif msg == '晚餐表格':
        dinner(event)

    elif msg == '睡前表格':
        sleep(event)

    elif msg == '總表':
        allForm(event)

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請點擊要使用的功能圖示'))

#健保卡辨識(加入會員)
def joinUs(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請上傳健保卡正面照片'))

    # linebot處理照片訊息
    @handler.add(MessageEvent, message=ImageMessage)
    def handle_image_message(event):

        # get user info & message
        LineID = event.source.user_id
        LineName = line_bot_api.get_profile(LineID).display_name
        messageID = event.message.id
        userInfo = LineID + LineName

        # get msg details
        print('msg from [', userInfo, ']')

        # 使用者傳送的照片
        message_content = line_bot_api.get_message_content(event.message.id)

        # 照片儲存名稱
        fileName = userInfo + '.jpg'

        # 儲存照片
        with open('./images/healthIDcard/{}'.format(fileName) , 'wb')as f:
            for chunk in message_content.iter_content():
                f.write(chunk)

        # 健保卡辨識
        linebot_reply = rec_func.cardRec(fileName)

        # Linebot回傳訊息給使用者
        if linebot_reply == '發生錯誤！請重新加入會員，謝謝!':
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=linebot_reply))

        else:
            line_bot_api.reply_message(event.reply_token,
                                       [TextSendMessage(text=linebot_reply),
                                        TemplateSendMessage(
                                            alt_text='確認樣板',
                                            template=ConfirmTemplate(
                                                text='請選擇要新增何種聯絡方式',
                                                actions=[MessageTemplateAction(  # 按鈕選項
                                                    label='電話號碼', text='電話號碼'),
                                                    MessageTemplateAction(label='手機號碼', text='手機號碼')]))])

#修改個人資料  --->  快速選單
def personalInfoupdate(event):
    try:
        message = TextSendMessage(
            text='請選擇您要修改的個人資料',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="電話號碼", text="電話號碼")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="手機號碼", text="手機號碼")
                    ),]))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

#電話
def telephone(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='請輸入電話號碼'))
#電話號碼
def telephoneNo(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='請輸入號碼(請含區碼)'))
#儲存電話號碼
def inserTellPhoneNo(event):
    # get user info & message
    LineID = event.source.user_id
    LineName = line_bot_api.get_profile(LineID).display_name
    userInfo = LineID + LineName
    msg = event.message.text

    loginInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': '使用者',
        'passwd': '密碼',
        'db': '資料庫',
        'charset': 'utf8mb4'
    }
    conn = pymysql.connect(**loginInfo)
    cursor = conn.cursor()
    # get msg details
    print('msg from [', userInfo, '] : ', msg)

    #要關閉才能修改
    sqlclose = """SET SQL_SAFE_UPDATES = 0;"""
    cursor.execute(sqlclose)

    sqlphoneno = (f""" UPDATE member_data
                    SET TELEPHONE = '{msg}'
                    where LINEID = '{LineID}';""")
    #保護開啟
    sqlopen = """SET SQL_SAFE_UPDATES = 1;"""

    cursor.execute(sqlphoneno)
    conn.commit()
    cursor.execute(sqlopen)

    cursor.close()
    conn.close()

    try:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='新增成功!若需修改，請點擊個人會員服務圖示，謝謝!'))
    except:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='發生錯誤，請重新輸入，謝謝!'))

#手機
def cellphone(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='請輸入手機號碼'))

#手機號碼
def cellphoneNo(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='請輸入號碼'))

#儲存手機號碼
def inserCellPhoneNo(event):
    # get user info & message
    LineID = event.source.user_id
    LineName = line_bot_api.get_profile(LineID).display_name
    userInfo = LineID + LineName
    msg = event.message.text

    # get msg details
    print('msg from [', userInfo, '] : ', msg)

    loginInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': '使用者',
        'passwd': '密碼',
        'db': '資料庫',
        'charset': 'utf8mb4'
    }
    conn = pymysql.connect(**loginInfo)
    cursor = conn.cursor()
    # 要關閉才能修改
    sqlclose = """SET SQL_SAFE_UPDATES = 0;"""
    cursor.execute(sqlclose)

    sqlphoneno = (f"""
                    UPDATE member_data
                    SET CELLPHONE = '{msg}'
                    where LINEID = '{LineID}';""")

    #保護開啟
    sqlclose = """SET SQL_SAFE_UPDATES = 1;"""

    cursor.execute(sqlopen)

    cursor.execute(sqlphoneno)
    conn.commit()

    cursor.close()
    conn.close()

    try:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='新增成功!若需修改，請點擊個人會員服務圖示，謝謝!'))
    except:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='發生錯誤，請重新輸入，謝謝!'))

#個人用藥查詢  --->  快速選單
def personal(event):
    try:
        message = TextSendMessage(
            text='請選擇您要查詢的用藥時間',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="早餐", text="早餐表格")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="午餐", text="午餐表格")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="晚餐", text="晚餐表格")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="睡前", text="睡前表格")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="總表", text="總表")
                    ),]))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

#早餐表格
def breakfast(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='早餐表格網址(NOT YET)'))

#午餐表格
def lunch(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='午餐表格網址(NOT YET)'))

#晚餐表格
def dinner(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='晚餐表格網址(NOT YET)'))

#睡前表格
def sleep(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='睡前表格網址(NOT YET)'))

#總表
def allForm(event):
    # get user info & message
    LineID = event.source.user_id
    LineName = line_bot_api.get_profile(LineID).display_name
    userInfo = LineID + LineName
    msg = event.message.text

    # get msg details
    print('msg from [', userInfo, '] : ', msg)

    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text='http://192.168.1.114:5000/show_notices'))




#其他會員服務  --->  按鈕樣版
def otherService(event):
    try:
        message = TemplateSendMessage(
            alt_text='其他會員服務',
            template=ButtonsTemplate(
                # thumbnail_image_url='https://i.imgur.com/IxvRLNX.png',  # 顯示的圖片
                title='其他會員服務',  # 主標題
                text='請選擇：',  # 副標題
                actions=[
                    MessageTemplateAction(   # 顯示文字計息
                        label='個人資料',
                        text='個人資料'),
                    MessageTemplateAction(  # 顯示文字計息
                        label='回診醫院',
                        text='回診醫院'),
                    URITemplateAction(  # 開啟網頁
                        label='聯絡藥師',
                        uri='(not yet)'),]))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


# 個人用藥查詢  --->  快速選單
def personalInfo(event):
    try:
        message = TextSendMessage(
            text='請選擇',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="查詢", text="查詢個人資料")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="修改", text="修改個人資料")
                    ),]))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


#查詢個人資料
def personalInfoSearsh(event):
    # get user info & message
    LineID = event.source.user_id
    LineName = line_bot_api.get_profile(LineID).display_name
    userInfo = LineID + LineName
    msg = event.message.text

    # get msg details
    print('msg from [', userInfo, '] : ', msg)

    loginInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': '使用者',
        'passwd': '密碼',
        'db': '資料庫',
        'charset': 'utf8mb4'
    }
    conn = pymysql.connect(**loginInfo)
    cursor = conn.cursor()

    sqlpersonalInfo = (f"""
        SELECT NAME,
        IDENTITY_NUMBER,
        BIRTH,
        HEALTH_NUMBER,
        TELEPHONE,
        CELLPHONE 
        FROM MEMBER_DATA
        WHERE LINEID = '{LineID}';
        """)

    cursor.execute(sqlpersonalInfo)
    data = cursor.fetchall()
    print((data))
    cursor.close()
    conn.close()

    output = []
    for row in data:
        for i in row:
            output.append(i)
    print(output)

    all = ''
    for r in range(len(output)):
        if r == 0:
            all += '姓名: ' + output[r] + '\n'
        elif r == 1:
            all += '身分證字號: ' + output[r] + '\n'
        elif r == 2:
            all += '生日: ' + output[r] + '\n'
        elif r == 3:
            all += '健保卡卡號: ' + output[r] + '\n'
        elif r == 4:
            all += '電話號碼: ' + output[r] + '\n'
        elif r == 5:
            all += '手機號碼: ' + output[r]

    try:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=all))
    except:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='發生錯誤，請重新輸入，謝謝!'))




#回診醫院  --->  圖片轉盤
def hospitalReserve(event):
    try:
        message = TemplateSendMessage(
            alt_text='回診醫院',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/LKocsE6.png',
                        action=URITemplateAction(  # 開啟網頁
                            label='三軍總醫院',
                            uri='https://www2.ndmctsgh.edu.tw/NewWebReg/'
                        )),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/JXLNEF6.png',
                        action=URITemplateAction(  # 開啟網頁
                            label='臺大醫院',
                            uri='https://reg.ntuh.gov.tw/WebAdministration/'
                        )),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/PBN6wXi.png',
                        action=URITemplateAction(  # 開啟網頁
                            label='台北榮總',
                            uri='https://www6.vghtpe.gov.tw/reg/queryForm.do?type=return'
                        ))]))

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

#好食推薦  --->  按鈕樣版
def greatFood(event):
    try:
        message = TemplateSendMessage(
            alt_text='好食推薦',
            template=ButtonsTemplate(
                # thumbnail_image_url='https://i.imgur.com/IxvRLNX.png',  # 顯示的圖片
                title='好食推薦',  # 主標題
                text='請選擇：',  # 副標題
                actions=[
                    URITemplateAction(  # 開啟網頁
                        label='台灣好農',
                        uri='https://www.wonderfulfood.com.tw/Client/index.aspx?gclid=CjwKCAjw8KmLBhB8EiwAQbqNoMBpNCPXW37NozfKKjzktX-wtvDjNvkB07c4HHvCb9SoLN4sYyuV3BoC3v4QAvD_BwE'
                    ),
                    MessageTemplateAction(  # 顯示文字計息
                        label='推薦食材',
                        text='推薦食材'
                    ),
                    MessageTemplateAction(  # 顯示文字計息
                        label='禁忌食材',
                        text='禁忌食材'
                    )]))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

#推薦食材
def recommendedFood(event):
    # get user info & message
    LineID = event.source.user_id
    LineName = line_bot_api.get_profile(LineID).display_name
    userInfo = LineID + LineName
    msg = event.message.text

    # get msg details
    print('msg from [', userInfo, '] : ', msg)

    loginInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': '使用者',
        'passwd': '密碼',
        'db': '資料庫',
        'charset': 'utf8mb4'
    }
    conn = pymysql.connect(**loginInfo)
    cursor = conn.cursor()

    sql = (f"""
             SELECT g.RecommendedIngredients
             FROM goodfood g join rx r on (g.DiseaseID = r.DiseaseID)
             where LINEID = '{LineID}';
             """)

    cursor.execute(sql)
    data = cursor.fetchall()
    output = []
    for row in data:
        for i in row:
            output.append(i)
    all = ''
    for i in range(len(output)):
        all += output[0]

    all = "高血壓推薦食材: " + all
    print(all)

    cursor.close()
    conn.close()

    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=all))


#處方箋辨識
def rxForm(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請上傳處方箋照片'))

    # linebot處理照片訊息
    @handler.add(MessageEvent, message=ImageMessage)

    def handle_image_message(event):
        # 使用者傳送的照片
        message_content = line_bot_api.get_message_content(event.message.id)

        # get user info & message
        LineID = event.source.user_id
        LineName = line_bot_api.get_profile(LineID).display_name
        userInfo = LineID + LineName

        # get msg details
        print('msg from [', userInfo, ']')

        # 使用者傳送的照片
        message_content = line_bot_api.get_message_content(event.message.id)

        # 照片儲存名稱
        fileName = userInfo + '.jpg'

        # 儲存照片
        with open('./images/prescriptionNote/{}'.format(fileName) , 'wb')as f:
            for chunk in message_content.iter_content():
                f.write(chunk)

        #影像辨識出的健保代碼
        results = str(re.findall("[A-Z]{2}\d{6}[G,\d]\d", text))

        # results = ['AC373441G0', 'BC24039100', 'AC57216100', 'AC41807100', 'BC23293100']
        result = str(results)
        result_str = result.replace("[", "").replace("]", "")

        loginInfo = {
            'host': 'localhost',
            'port': 3306,
            'user': '使用者',
            'passwd': '密碼',
            'db': '資料庫',
            'charset': 'utf8mb4'
        }
        conn = pymysql.connect(**loginInfo)
        cursor = conn.cursor()

        sql = (f"""
        SELECT DRUG_NO,
                EGNAME,
                CNNAME,
                CLINICALUSE,
                SIDEEFFECTS,
                STORAGEMETHOD,
                DRUGNOTE,
                OTHER,
                PIC 
        FROM NOTICES
        WHERE DRUG_NO IN ({result_str});
        """)

        cursor.execute(sql)
        data = cursor.fetchall()

        output = []
        for row in data:
            for i in row:
                output.append(i)

        all = ''
        for r in range(len(output)):
            if r % 9 == 0:
                all += '藥品代碼: ' + output[r] + '\n' + '\n'
            elif r % 9 == 1:
                all += '英文名: ' + output[r] + '\n' + '\n'
            elif r % 9 == 2:
                all += '中文名: ' + output[r] + '\n' + '\n'
            elif r % 9 == 3:
                all += '臨床用途: ' + output[r] + '\n' + '\n'
            elif r % 9 == 4:
                all += '主要副作用: ' + output[r] + '\n' + '\n'
            elif r % 9 == 5:
                all += '儲存方式: ' + output[r] + '\n' + '\n'
            elif r % 9 == 6:
                all += '用要注意: ' + output[r] + '\n' + '\n'
            elif r % 9 == 7:
                all += '其他說明: ' + output[r] + '\n' + '\n'
            else:
                all += '圖片: ' + output[r] + '\n' + "======================" + '\n' + '\n'


        cursor.close()
        conn.close()

        print(all)

        #回傳藥品代碼及相關資料
        try:
            line_bot_api.reply_message(event.reply_token,
                                       [TextSendMessage(text=all),
                                       TemplateSendMessage(
                                            alt_text='確認樣板',
                                            template=ConfirmTemplate(
                                                text='是否再繼續上傳新的處方箋？',
                                                actions=[MessageTemplateAction(  #按鈕選項
                                                        label='是',text='請再次點選處方箋辨識功能圖示'),
                                                    MessageTemplateAction(label='否',text='您的處方箋已成功上傳')]))])
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！請重新點選處方箋辨識功能圖示，再重新上傳圖片，謝謝!'))

#藥物交互作用
def drugInteractions(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='http://192.168.1.114:5000/show_interaction'))


if __name__ == '__main__':
    app.run(port=12345)
