import pymysql


from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
import re
import pymysql
from pymysql.converters import escape_string

# Azure Form Recognizer
endpoint = "https://testtestform.cognitiveservices.azure.com/"
credential = AzureKeyCredential("f6614bd9ebf34a389deb587931c59d71")
form_recognizer_client = FormRecognizerClient(endpoint, credential)


with open(r"sign4.JPG", "rb") as fd:
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
result = str(list(filter(regex.match, datas)))

print(result)
print(type(result))


def getNotices():
    host = 'localhost'
    port = 3306
    user = 'root'
    passwd = '0905'
    db = 'TFB103_G2'
    charset = 'utf8mb4'

    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor()
    result_str = result.replace("[", "").replace("]", "")
    print(result_str)

    sql = (f"""
    SELECT DRUGCODE,
            EGNAME,
            CNNAME,
            CLINICALUSE,
            SIDEEFFECTS,
            STORAGEMETHOD,
            DRUGNOTE,
            OTHER 
    FROM NOTICES
    WHERE DRUGCODE IN ({result_str});
    """)


    cursor.execute(sql)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

if __name__ == '__main__':
    for r in getNotices():
        print(r)