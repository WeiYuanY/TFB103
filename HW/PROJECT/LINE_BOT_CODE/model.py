import pymysql
from datetime import datetime

#總表
def getNotices():
    host = 'localhost'
    port = 3306
    user = '使用者'
    passwd = '密碼'
    db = '資料庫'
    charset = 'utf8mb4'

    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor()
    today = datetime.today()
    month = today.month
    lastmonth = month - 1
    strmonth = str(month)
    strlastmonth = str(lastmonth)
    months = ('\'' + f'{strmonth}'+ '\''  + ',' + '\'' + f'{strlastmonth}') + '\''
    print(months)
    print(type(months))

    #還沒解決錯誤，先用訂值呈現
    NEWID = 'V120850998'

    sql = (f"""SELECT distinct n.DRUG_NO, n.EGNAME, n.CNNAME, n.DRUGNOTE, d.Drug_Fre_Name, d.Drug_Fre_Name_Time
    FROM notices n join newoutpatientrecords o on(n.DRUG_NO = o.DRUG_NO) join drugusefre d on (o.Drug_Fre = d.Drug_Fre)
    where NEWID = '{NEWID}' and FEE_M in ({months});
    """)


    cursor.execute(sql)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


if __name__ == '__main__':
    for r in getNotices():
        print(r)