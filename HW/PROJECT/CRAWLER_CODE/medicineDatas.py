import requests
from bs4 import BeautifulSoup
import os
import json
import os
import re

if not os.path.exists('./AllDatas'):
    os.mkdir("./AllDatas")

if not os.path.exists('./Information'):
    os.mkdir("./Information")

if not os.path.exists('./Characteristics'):
    os.mkdir("./Characteristics")

if not os.path.exists('./Notices'):
    os.mkdir("./Notices")

if not os.path.exists('./Notices1'):
    os.mkdir("./Notices1")

if not os.path.exists('./Pharmacy'):
    os.mkdir("./Pharmacy")

if not os.path.exists('./Injection'):
    os.mkdir("./Injection")

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
headers = {
"User-Agent": userAgent ,"Referer" : "https://www3.vghtc.gov.tw:8443/pharmacyHandbook/handbook.html"
}

url = 'https://www3.vghtc.gov.tw:8443/pharmacyHandbook/API/handbookSearch.jsp?adr=true&atc=true&code=true&comp=true&indication=true&keyword=*&pharNm=true&phar_e=true&trdNm=true'


res = requests.get(url,headers=headers)
print(res.text)
jsonData = res.json()
print(type(jsonData))
print(len(jsonData))
for i in range(len(jsonData)):

    #ID(藥碼)
    try:
        drugId = jsonData[i]['UDNDRGCODE']
    except KeyError:
        drugId = "無"

    #學名
    try:
        scientificName = jsonData[i]['UDNMATDGNM']
    except KeyError:
        scientificName = "無"

    #英文名
    try:
        egName = jsonData[i]['UDNMFTDGNM']
    except KeyError:
        egName = "無"

    #中文名
    try:
        cnName = jsonData[i]['UDDRGNMKJ']
    except KeyError:
        cnName = "無"

    #藥袋名
    try:
        bagName = jsonData[i]['UDDMDPNAME']
    except KeyError:
        bagName = "無"

    #健保碼
    try:
        drugCode = jsonData[i]['UDNNHICODE']
    except KeyError:
        drugCode = ""

# -------------------------------------------------------------------------------------------------------------

    newUrl = 'https://www3.vghtc.gov.tw:8443/pharmacyHandbook/API/handbookData.jsp?code=' + drugId
    newHeaders = {
        "User-Agent": userAgent,
        "Referer": f'https://www3.vghtc.gov.tw:8443/pharmacyHandbook/handbook.html#/data/{drugId}'}

    newRes = requests.get(newUrl, headers=newHeaders)
    newJsonData = newRes.json()


    #劑型
    try:
        dosageForm = newJsonData['UDDDOSFORM']
    except KeyError:
        dosageForm = ""

    #規格
    try:
        format = newJsonData['SUPPLY']
    except KeyError:
        format = ""

    #成分碼
    try:
        ingredientCode1 = newJsonData['DRUGCOMP'][0]['code']
    except KeyError:
        ingredientCode1 = ""
    except IndexError:
        ingredientCode1 = ""
    try:
        ingredientCode2 = newJsonData['DRUGCOMP'][1]['code']
    except KeyError:
        ingredientCode2 = ""
    except IndexError:
        ingredientCode2 = ""

    ingredientCode = ingredientCode1 + ingredientCode2

    #成分名
    try:
        ingredientName1 = newJsonData['DRUGCOMP'][0]['name']
    except KeyError:
        ingredientName1 = ""
    except IndexError:
        ingredientName1 = ""
    try:
        ingredientName2= newJsonData['DRUGCOMP'][1]['name']
    except KeyError:
        ingredientName2 = ""
    except IndexError:
        ingredientName2 = ""

    ingredientName = ingredientName1 + ingredientName2

    #藥理分類
    try:
        pharmacologicalClassification1 = newJsonData['UDDCATAG'][0]['phar_e']
    except KeyError:
        pharmacologicalClassification1 = ""
    try:
        pharmacologicalClassification2 = newJsonData['UDDCATAG'][0]['phar_c']
    except KeyError:
        pharmacologicalClassification2 = ""

    pharmacologicalClassification = pharmacologicalClassification1 + pharmacologicalClassification2

    #ATC碼
    try:
        atcCode = newJsonData['UDDATC'][0]['code']
    except KeyError:
        atcCode = ""

    # -------------------------------------------------------------------------------------------------------------

    #適應症
    try:
        Indications = newJsonData['INDICATION']
    except KeyError:
        Indications = ""

    #藥理
    try:
        pharmacology = newJsonData['PHARMACOLOGY']
    except KeyError:
        pharmacology = ""

    #藥動學
    try:
        pharmacokinetics = newJsonData['PHARMACOKINETICS']
    except KeyError:
        pharmacokinetics = ""

    #禁忌症
    try:
        contraindications = newJsonData['CONTRAINDICATION']
    except KeyError:
        contraindications = ""


    #年長者
    try:
        elder = newJsonData['BEER_CRITERIA'][0]
    except KeyError:
        elder = ""
    except IndexError:
        elder = ""

    #懷孕分類
    try:
        pregnantLevel = newJsonData['UDDPRGLEVEL']
    except KeyError:
        pregnantLevel = ""

    #哺乳分類 breastfeedingClassification
    try:
        breastfeedingClassification = newJsonData['BREAST_MILK_FEEDING']
    except KeyError:
        breastfeedingClassification = ""

    #副作用
    try:
        sideEffects = newJsonData['BAG']['ADVERSE_REACTION']
    except KeyError:
        sideEffects = ""

    #劑量和給藥方法
    try:
        dosageAndAdministration = newJsonData['DOSAGE_AND_ADMINISTRATION']
    except KeyError:
        dosageAndAdministration = ""
    except IndexError:
        dosageAndAdministration = ""

    #小兒調整劑量
    try:
        children = newJsonData['DOSE_PED']
    except KeyError:
        children = ""

    #腎功能調整劑量
    try:
        renal = newJsonData['DOSE_RENAL']
    except KeyError:
        renal = ""

    #肝功能調整劑量
    try:
        liver = newJsonData['DOSE_LIVER']
    except KeyError:
        liver = ""

    #注意事項
    try:
        notice = newJsonData['DRUG_CAUTION']
    except KeyError:
        notice = ""

    #磨粉建議
    try:
        powder = newJsonData['DRUG_POWDER']
    except KeyError:
        powder = ""

    # -------------------------------------------------------------------------------------------------------------

    #臨床用途
    try:
        use = newJsonData['BAG']['INDICATION']
    except KeyError:
        use = ""

    #主要副作用
    try:
        mainSideEffects = newJsonData['BAG']['SIDEEFFECT']
    except KeyError:
        mainSideEffects = ""

    # 儲存方式
    try:
        storage = newJsonData['BAG']['STORAGE']
    except KeyError:
        storage = ""

    #用藥注意
    try:
        medicationTime = newJsonData['BAG']['LABEL']
    except KeyError:
        medicationTime = ""

    #其他說明
    try:
        otherInstructions = newJsonData['BAG']['OTHER']
    except KeyError:
        otherInstructions = ""

# -------------------------------------------------------------------------------------------------------------
    #給藥途徑
    try:
        route = newJsonData['INJECT']['INJ_ROUTE']
    except KeyError:
        route = ""

    #靜脈輸注液
    try:
        vein = newJsonData['INJECT']['INJ_SOLN']
    except KeyError:
        vein = ""

    #每瓶稀釋液體積
    try:
        volume = newJsonData['INJECT']['INJ_VOLUME']
    except KeyError:
        volume = ""

    #給藥濃度
    try:
        concentration = newJsonData['INJECT']['INJ_CONC']
    except KeyError:
        concentration = ""

    #給藥速率
    try:
        rate = newJsonData['INJECT']['INJ_RATE']
    except KeyError:
        rate = ""

    # #安定性
    # try:
    #     route = newJsonData['INJECT']['INJ_ROUTE']
    # except KeyError:
    #     route = ""

    #注意事項
    try:
        injectNotice = newJsonData['INJECT']['INJ_CAUTION']
    except KeyError:
        injectNotice = ""




# -------------------------------------------------------------------------------------------------------------

    #顏色
    try:
        color = newJsonData['UDNCLR1']
    except KeyError:
        color = ""

    #形狀
    try:
        shape = newJsonData['UDNSHP']
    except KeyError:
        shape = ""

    # 剝痕
    try:
        notch = newJsonData['UDNNTCH']
    except KeyError:
        notch = ""

    #標記1
    try:
        mark1 = newJsonData['UDNMARK1']
    except KeyError:
        mark1 = ""

    #標記2
    try:
        mark2 = newJsonData['UDNMARK2']
    except KeyError:
        mark2 = ""

    # 藥品圖片
    drugPic = 'https://www3.vghtc.gov.tw:8443/pharmacyHandbook/API/getImage.jsp?path=pic&code=' + drugId

    # 外觀圖片
    appearancePic = 'https://www3.vghtc.gov.tw:8443/pharmacyHandbook/API/getImage.jsp?path=out&code=' + drugId

# -------------------------------------------------------------------------------------------------------------

    newUrl_1 = "https://www3.vghtc.gov.tw:8443/pharmacyHandbook/API/handbookDataEducation.jsp?code=" + drugId
    newHeaders_1 = {
        "User-Agent": userAgent,
        "Referer" : f'https://www3.vghtc.gov.tw:8443/pharmacyHandbook/education/#/data/{drugId}'}
    newRes1 = requests.get(newUrl_1, headers=newHeaders_1)
    newJsonData_1 = newRes1.json()


    #臨床用途
    try:
        use1 = newJsonData_1['DATA']['INDICATION_EDU']
    except KeyError:
        use1 = ''

    #主要副作用
    try:
        mainSideEffects1 = newJsonData_1['DATA']['ADVERSE_REACTION_EDU']
    except KeyError:
        mainSideEffects1 = ''

    #用藥須知
    try:
        notice1 = newJsonData_1['DATA']['CAUTION_EDU']
    except KeyError:
        notice1 = ''

    #如何正確用藥
    try:
        drugUse = newJsonData_1['DATA']['DRUG_USE_EDU']
    except KeyError:
        drugUse = ''

    #如何保存藥品
    try:
        storage1 = newJsonData_1['DATA']['STORAGE_EDU']
    except KeyError:
        storage1 = ''

#--------------------------------------------------------------------------------------------------------------

    informationData = ""
    informationData += 'ID: ' + drugId + '\n*'
    informationData += '學名: ' + scientificName + '\n*'
    informationData += '英文名: ' + egName + '\n*'
    informationData += '中文名: ' + cnName + '\n*'
    informationData += '藥袋名: ' + bagName + '\n*'
    informationData += '劑型: ' + dosageForm + '\n*'
    informationData += '規格: ' + format + '\n*'
    informationData += '成分碼: ' + ingredientCode + '\n*'
    informationData += '成分名: ' + ingredientName + '\n*'
    informationData += '藥理分類: ' + pharmacologicalClassification + '\n*'
    informationData += '健保代碼: ' + drugCode + '\n*'
    informationData += 'ATC碼: ' + atcCode

    informationDatas = re.sub('<(.|/n)+?>','',informationData).replace('&nbsp;','').replace('&lt;','<').replace('&quot;','"').replace('&ge;','≥').replace('&sim;','∼').replace('&deg;','°C')

    with open("./Information/{}.txt".format(drugCode), "w", encoding="utf-8") as f:
        f.write(informationDatas)

# #-------------------------------------------------------------------------------------------------------------

    characteristicsData = ""
    characteristicsData += '健保代碼: ' + drugCode + '\n*'
    characteristicsData += '藥袋名: ' + bagName + '\n*'
    characteristicsData += '中文名: ' + cnName + '\n*'
    characteristicsData += '顏色: ' + color + '\n*'
    characteristicsData += '形狀: ' + shape + '\n*'
    characteristicsData += '剝痕: ' + notch + '\n*'
    characteristicsData += '標記1: ' + mark1 + '\n*'
    characteristicsData += '標記2: ' + mark2 + '\n*'
    characteristicsData += '藥品圖片: ' + drugPic + '\n*'
    characteristicsData += '外觀圖片: ' + appearancePic

    characteristicsDatas = re.sub('<(.|/n)+?>','',characteristicsData).replace('&nbsp;','').replace('&lt;','<').replace('&quot;','"').replace('&ge;','≥').replace('&sim;','∼').replace('&deg;','°C')

    with open("./Characteristics/{}.txt".format(drugCode), "w", encoding="utf-8") as f:
        f.write(characteristicsDatas)

# # -------------------------------------------------------------------------------------------------------------

    noticesData = ''
    noticesData += '健保代碼: ' + drugCode + '\n*'
    noticesData += '藥袋名: ' + bagName + '\n*'
    noticesData += '中文名: ' + cnName + '\n*'
    noticesData += '臨床用途: ' + use + '\n*'
    noticesData += '主要副作用: ' + mainSideEffects + '\n*'
    noticesData += '儲存方式: ' + storage + '\n*'
    noticesData += '用藥注意: ' + medicationTime + '\n*'
    noticesData += '其他說明: ' + otherInstructions + '\n*'

    noticesDatas = re.sub('<(.|/n)+?>','',noticesData).replace('&nbsp;','').replace('&lt;','<').replace('&quot;','"').replace('&ge;','≥').replace('&sim;','∼').replace('&deg;','°C')

    with open("./Notices/{}.txt".format(drugCode), "w", encoding="utf-8") as f:
        f.write(noticesDatas)

# #-------------------------------------------------------------------------------------------------------------

    pharmacyData = ""
    pharmacyData += '健保代碼: ' + drugCode + '\n*'
    pharmacyData += '學名: ' + scientificName + '\n*'
    pharmacyData += '適應症: ' + Indications + '\n*'
    pharmacyData += '藥理: ' + pharmacology + '\n*'
    pharmacyData += '藥動學: ' + pharmacokinetics + '\n*'
    pharmacyData += '禁忌症: ' + contraindications + '\n*'
    pharmacyData += '年長者: ' + elder + '\n*'
    pharmacyData += '懷孕分類: ' + pregnantLevel + '\n*'
    pharmacyData += '哺乳分類: ' + breastfeedingClassification + '\n*'
    pharmacyData += '副作用: ' + sideEffects + '\n*'
    pharmacyData += '劑量和給藥方法: ' + dosageAndAdministration + '\n*'
    pharmacyData += '小兒調整劑量: ' + children + '\n*'
    pharmacyData += '腎功能調整劑量: ' + renal + '\n*'
    pharmacyData += '肝功能調整劑量: ' + liver + '\n*'
    pharmacyData += '磨粉建議: ' + powder + '\n*'
    pharmacyData += "注意事項: " + notice

    pharmacyDatas = re.sub('<(.|/n)+?>','',pharmacyData).replace('&nbsp;','').replace('&lt;','<').replace('&quot;','"').replace('&ge;','≥').replace('&sim;','∼').replace('&deg;','°C')

    with open("./Pharmacy/{}.txt".format(drugCode), "w", encoding="utf-8") as f:
        f.write(pharmacyDatas)

#-----------------------------------------------------------------------------------------------------------------

    injectionData = ""
    injectionData += '健保代碼: ' + drugCode + '\n*'
    injectionData += '學名: ' + scientificName + '\n*'
    injectionData += '給藥途徑: ' + route + '\n*'
    injectionData += '靜脈輸注液: ' + vein + '\n*'
    injectionData += '每瓶稀釋液體積: ' + volume + '\n*'
    injectionData += '給藥濃度: ' + concentration + '\n*'
    injectionData += '給藥速率: ' + rate + '\n*'
    injectionData += '注意事項: ' + injectNotice

    injectionDatas = re.sub('<(.|/n)+?>','',injectionData).replace('&nbsp;','').replace('&lt;','<').replace('&quot;','"').replace('&ge;','≥').replace('&sim;','∼').replace('&deg;','°C')

    with open("./Injection/{}.txt".format(drugCode), "w", encoding="utf-8") as f:
        f.write(injectionDatas)

# -----------------------------------------------------------------------------------------------------------------

    noticesData_1 = ""
    noticesData_1 += '健保代碼: ' + drugCode + '\n*'
    noticesData_1 += '藥袋名: ' + bagName + '\n*'
    noticesData_1 += '中文名: ' + cnName + '\n*'
    noticesData_1 += '臨床用途: ' + use1 + '\n*'
    noticesData_1 += '主要副作用: ' + mainSideEffects1 + '\n*'
    noticesData_1 += '用藥須知: ' + notice1 + '\n*'
    noticesData_1 += '如何正確用藥: ' + drugUse + '\n*'
    noticesData_1 += '如何保存藥品: ' + storage1  + '\n*'
    noticesData_1 += '藥品圖片: ' + drugPic

    noticesDatas_1 = re.sub('<(.|/n)+?>','',noticesData_1).replace('&nbsp;','').replace('&lt;','<').replace('&quot;','"').replace('&ge;','≥').replace('&sim;','∼').replace('&deg;','°C')


    with open("./Notices1/{}.txt".format(drugCode), "w", encoding="utf-8") as f:
        f.write(noticesDatas_1)


# #-----------------------------------------------------------------------------------------------

    medicineData = ""
    medicineData += 'ID: ' + drugId + '\n*'
    medicineData += '學名: ' + scientificName + '\n*'
    medicineData += '英文名: ' + egName + '\n*'
    medicineData += '中文名: ' + cnName + '\n*'
    medicineData += '藥袋名: ' + bagName + '\n*'
    medicineData += '劑型: ' + dosageForm + '\n*'
    medicineData += '規格: ' + format + '\n*'
    medicineData += '成分碼: ' + ingredientCode + '\n*'
    medicineData += '成分名: ' + ingredientName + '\n*'
    medicineData += '藥理分類: ' + pharmacologicalClassification + '\n*'
    medicineData += '健保代碼: ' + drugCode + '\n*'
    medicineData += 'ATC碼: ' + atcCode + '\n*'

    medicineData += '適應症: ' + Indications + '\n*'
    medicineData += '藥理: ' + pharmacology + '\n*'
    medicineData += '藥動學: ' + pharmacokinetics + '\n*'
    medicineData += '禁忌症: ' + contraindications + '\n*'
    medicineData += '年長者: ' + elder + '\n*'
    medicineData += '懷孕分類: ' + pregnantLevel + '\n*'
    medicineData += '哺乳分類: ' + breastfeedingClassification + '\n*'
    medicineData += '副作用: ' + sideEffects + '\n*'
    medicineData += '劑量和給藥方法: ' + dosageAndAdministration + '\n*'
    medicineData += '小兒調整劑量: ' + children + '\n*'
    medicineData += '腎功能調整劑量: ' + renal + '\n*'
    medicineData += '肝功能調整劑量: ' + liver + '\n*'
    medicineData += "注意事項: " + notice + '\n*'
    medicineData += '磨粉建議: ' + powder + '\n*'

    medicineData += '臨床用途: ' + use + '\n*'
    medicineData += '主要副作用: ' + mainSideEffects + '\n*'
    medicineData += '儲存方式: ' + storage + '\n*'
    medicineData += '用藥注意: ' + medicationTime + '\n*'
    medicineData += '其他說明: ' + otherInstructions + '\n*'

    medicineData += '給藥途徑: ' + route + '\n*'
    medicineData += '靜脈輸注液: ' + vein + '\n*'
    medicineData += '每瓶稀釋液體積: ' + volume + '\n*'
    medicineData += '給藥濃度: ' + concentration + '\n*'
    medicineData += '給藥速率: ' + rate + '\n*'
    medicineData += '注意事項: ' + injectNotice + '\n*'

    medicineData += '臨床用途: ' + use1 + '\n*'
    medicineData += '主要副作用: ' + mainSideEffects1 + '\n*'
    medicineData += '用藥須知: ' + notice1 + '\n*'
    medicineData += '如何正確用藥: ' + drugUse + '\n*'
    medicineData += '如何保存藥品: ' + storage1 + '\n*'

    medicineData += '顏色: ' + color + '\n*'
    medicineData += '形狀: ' + shape + '\n*'
    medicineData += '剝痕: ' + notch + '\n*'
    medicineData += '標記1: ' + mark1 + '\n*'
    medicineData += '標記2: ' + mark2 + '\n*'

    medicineData += '藥品圖片: ' + drugPic + '\n*'
    medicineData += '外觀圖片: ' + appearancePic + '\n*'

    medicineData += '臨床用途: ' + use1 + '\n*'
    medicineData += '主要副作用: ' + mainSideEffects1 + '\n*'
    medicineData += '用藥須知: ' + notice1 + '\n*'
    medicineData += '如何正確用藥: ' + drugUse + '\n*'
    medicineData += '如何保存藥品: ' + storage1

    medicineDatas = re.sub('<(.|/n)+?>','',medicineData).replace('&nbsp;','').replace('&lt;','<').replace('&quot;','"').replace('&ge;','≥').replace('&sim;','∼').replace('&deg;','°C')

    print(medicineDatas)
    print('=====================')
    with open("./AllDatas/{}.txt".format(drugCode), "w", encoding="utf-8") as f:
        f.write(medicineDatas)


