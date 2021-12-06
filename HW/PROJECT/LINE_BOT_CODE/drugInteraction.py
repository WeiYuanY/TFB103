import pandas as pd
import pymysql
import re
import time
from datetime import datetime

start_time = time.time()
def getInteracion(ID):
    df = pd.read_csv("NIHdrugbankall.csv",sep="\t",encoding='latin1')
    ref = pd.read_csv("all.csv")
    ref.drop_duplicates(subset = ['inter_type'], keep = 'first',inplace = True)
    today = datetime.today()
    month = today.month
    lastmonth = month - 1
    strmonth = str(month)
    strlastmonth = str(lastmonth)
    months = ('\'' + f'{strmonth}' + '\'' + ',' + '\'' + f'{strlastmonth}') + '\''

    host = 'localhost'
    port = 3306
    user = '使用者'
    passwd = '密碼'
    db = '資料庫'
    charset = 'utf8mb4'

    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor()

    sqlID = (f"""SELECT DRUG_NO FROM newoutpatientrecords
             where NEWID = '{ID}'and FEE_M in ({months});""")
    cursor.execute(sqlID)
    results = cursor.fetchall()

    resultLIST = []
    for u in range(len(results)):
        resultLIST.append(str(results[u]).replace('\',)','').replace(')','').replace('(\'',''))

    print(len(resultLIST))
    print(resultLIST)

    # 轉換藥物代碼
    def N_to_id(drugN):
        for i in range(df.shape[0]):
            if drugN == df["N"][i]:
                drug = df["drugbankid"][i]
                return drug
    my_drug_id = list(map(N_to_id, resultLIST))
    print(my_drug_id)
    drugIds=[]
    interDrugIds=[]
    for x in my_drug_id:
        for y in my_drug_id:
            my_filter1 = ref["drug_id"] == x
            my_filter2 = ref["inter_drug_id"] == y
            interaction = ref[my_filter1 & my_filter2]
            drugId = interaction["drug_id"]
            interDrugId = interaction["inter_drug_id"]
            if len(drugId) != 0:
                drugIds.append(drugId)
            if len(interDrugId) != 0:
                interDrugIds.append(interDrugId)

    drugIdDatas = []
    for s in range(len(drugIds)):
        data = str(drugIds[s])
        result = (re.findall('[A-Z]{2}\d{5}',data))
        drugIdDatas.append(result)

    interDrugIdDatas = []
    for s in range(len(interDrugIds)):
        data = str(interDrugIds[s])
        result = (re.findall('[A-Z]{2}\d{5}',data))
        interDrugIdDatas.append(result)


    drugIdResults = str(drugIdDatas).replace('[', '').replace(']', '')
    interDrugIdResults = str(interDrugIdDatas).replace('[', '').replace(']', '')

    host = 'localhost'
    port = 3306
    user = '使用者'
    passwd = '密碼'
    db = '資料庫'
    charset = 'utf8mb4'

    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor()

    sql = (f"""SELECT DRUGNAME, INTERDRUG,INTERTYPE FROM interaction
    
              where DRUGID in ({drugIdResults}) and INTERDRUGID in({interDrugIdResults}) ;""")

    cursor.execute(sql)
    interactiontResult = cursor.fetchall()

    cursor.close()
    conn.close()
    print(interactiontResult)
    print(time.time() - start_time)
    return interactiontResult


if __name__ == '__main__':
    for t in getInteracion():
        print(t)