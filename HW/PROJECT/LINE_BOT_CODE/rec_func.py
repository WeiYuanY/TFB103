import paddle
from paddleocr import PaddleOCR
import re
import os
import pymysql
from datetime import datetime


############### 健保卡辨識功能 ###############

def cardRec(img):
    # def cardRec(img):

    # 選擇要使用的模型
    ocr = PaddleOCR(
        rec_model_dir=r'C:\Users\user\PycharmProjects\TFB103_02_Project\rec_chinese_cht_mobile_inference_final',
        rec_char_dict_path=r'C:\Users\user\PycharmProjects\TFB103_02_Project\ppocr\utils\dict\chinese_cht_dict.txt',
        use_gpu=False, )

    # 選擇識別的圖片
    local_image_path = os.getcwd() + '/images/healthIDcard/' + '//' + img
    result = ocr.ocr(local_image_path, cls=True)

    # 建立需要的資料
    text = ''
    for i in result:
        text = text + i[1][0] + ','

    Time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Name = str(re.findall(",[\u4e00-\u9fa5]{3},", text)).replace(',','').replace('[', '').replace(']', '').replace("'", '')
    Identity_number = str(re.findall("[A-Z]{1}[\d]{9}", text)).replace('[','').replace(']', '').replace("'", '')
    Birth = str(re.findall(",[\d]{,3}/[\d]{2}/[\d]{2},", text)).replace(',','').replace('[', '').replace(']', '').replace("'", '')
    Health_number = str(re.findall(",[0]{4}[\d]{8},", text)).replace(',','').replace('[', '').replace(']', '').replace("'", '')
    File_path = img

    LineID = File_path[0:33]
    LineName = File_path[33:-4]
    TELEPHONE = "Null"
    CELLPHONE = "Null"



    # 會員資料存入MySQL
    db = pymysql.connect(host='localhost', user='使用者', passwd='密碼',
                         db='資料庫', charset='utf8')
    cursor = db.cursor()

    if Name != '':
        query = 'INSERT INTO member_data (TIME, NAME, IDENTITY_NUMBER, BIRTH, HEALTH_NUMBER, FILE_PATH ,LINEID, LINENAME, TELEPHONE, CELLPHONE) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)'
        value = (
        Time, Name, Identity_number, Birth, Health_number, File_path, LineID,
        LineName, TELEPHONE, CELLPHONE)

        cursor.execute(query, value)
        db.commit()
        cardMSG = f'Hi {Name}, 已將您的資料存入會員檔案裡 ~~'

    else:
        db.rollback()
        cardMSG = '發生錯誤！請重新加入會員，謝謝!'

    db.close()

    return cardMSG


############### 處方簽辨識功能 ###############

def signRec(img):
    # 選擇要使用的模型
    ocr = PaddleOCR(
        rec_model_dir=r'C:\Users\user\PycharmProjects\TFB103_02_Project\rec_chinese_cht_mobile_inference_final',
        rec_char_dict_path=r'C:\Users\user\PycharmProjects\TFB103_02_Project\ppocr\utils\dict\chinese_cht_dict.txt',
        use_gpu=False, )

    # 選擇識別的圖片
    # local_image_path = os.getcwd() +'/images/prescriptionNote/'+ '//' + img
    local_image_path = os.getcwd() + '//' + img
    result = ocr.ocr(local_image_path, cls=True)

    # 建立需要的資料
    text = ''
    for i in result:
        text = text + i[1][0] + ','
    #
    Time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    File_path = img


    Hospital_code = str(re.findall("[0][5][0]\d{7}", text)).replace(',','').replace('[', '').replace(']', '').replace("'", '')
    Health_code = str(re.findall("[A-Z]{2}\d{6}[G,\d]\d", text))
    Diagnosis = str(re.findall("高血壓", text)).replace(',', '').replace('[','').replace(']', '').replace("'", '')
    firstRounds = str(re.findall("[\d]{3}/[\d]{2}/[\d]{2}", text)).replace(',','').replace('[', '').replace(']', '').replace("'", '')
    nextRounds = str(re.findall(",\d{3}[年]\d{2}[月]\d{2}[日]", text)).replace(',''').replace('[', '').replace(']', '').replace("'", '')

    print(f'Time ={Time}')
    print(f'Hospital_code={Hospital_code}')
    print(f'Health_code={Health_code}')
    print(f'Diagnosis={Diagnosis}')
    print(f'First_Rounds={firstRounds}')
    print(f'Next_Rounds={nextRounds}')
    print(f'File_path={File_path}')

    # # 健保代碼抓取MySQL資料
    #
    # host = 'localhost'
    # port = 3306
    # user = '使用者'
    # passwd = '密碼'
    # db = '資料庫'
    # charset = 'utf8mb4'
    #
    # conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    # cursor = conn.cursor()
    # result_str = Health_code.replace("[", "").replace("]", "")
    #
    # sql = (f"""
    # SELECT DRUGCODE,
    #         EGNAME,
    #         CNNAME,
    #         CLINICALUSE,
    #         SIDEEFFECTS,
    #         STORAGEMETHOD,
    #         DRUGNOTE,
    #         OTHER,
    #         PIC
    # FROM NOTICES
    # WHERE DRUGCODE IN ({result_str});
    # """)
    #
    # cursor.execute(sql)
    # data = cursor.fetchall()
    #
    # cursor.close()
    # conn.close()
    #
    # # 建立回傳linebot資料
    #
    # output = []
    # for row in data:
    #     for i in row:
    #         output.append(i)
    #
    # signMSG = ''
    # for r in range(len(output)):
    #     if r % 9 == 0:
    #         signMSG += '藥品代碼: ' + output[r] + '\n' + '\n'
    #     elif r % 9 == 1:
    #         signMSG += '英文名: ' + output[r] + '\n' + '\n'
    #     elif r % 9 == 2:
    #         signMSG += '中文名: ' + output[r] + '\n' + '\n'
    #     elif r % 9 == 3:
    #         signMSG += '臨床用途: ' + output[r] + '\n' + '\n'
    #     elif r % 9 == 4:
    #         signMSG += '主要副作用: ' + output[r] + '\n' + '\n'
    #     elif r % 9 == 5:
    #         signMSG += '儲存方式: ' + output[r] + '\n' + '\n'
    #     elif r % 9 == 6:
    #         signMSG += '用要注意: ' + output[r] + '\n' + '\n'
    #     elif r % 9 == 7:
    #         signMSG += '其他說明: ' + output[r] + '\n' + '\n'
    #     else:
    #         signMSG += '圖片: ' + output[r] + '\n' + "======================" + '\n' + '\n'

    signMSG = "OK"
    return signMSG