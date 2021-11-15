import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('./food_med'):
 os.mkdir("./food_med")

url = 'https://www.edh.tw/tag/高血壓/{}'
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

headers = { "User-Agent" : userAgent ,"Referer" : 'https://www.edh.tw/'}

page = 1
for i in range(1,80):
    res = requests.get(url.format(page), headers = headers)
    soup =BeautifulSoup (res.text, 'html.parser')
    ids = soup.select('h3[class="title"]')

    # print(ids)
    # print('=======')

    #取各篇文章之ID、標題
    for id in ids:
        idNo = id.select('a')[0]['href'].split('/article/')[-1]
        title = id.select('a')[0].text
        if len(idNo) > 5 :
            continue
        else:
            idNo = id.select('a')[0]['href'].split('/article/')[-1]
            title = id.select('a')[0].text

        # print(idNo)
        # print(title)
        # print(len(idNo))
        #
        # #過濾media_article
        # if len(idNo) > 5:
        #     idNo

        name = idNo + ' ' + title
        print(name)
        # print(idNos)
        # print(title)
        # print('=============')


        newUrl = f'https://www.edh.tw/article/{idNo}'
        newRes = requests.get(newUrl,headers=headers)
        newSoup = BeautifulSoup(newRes.text,"html.parser")
        # print(newSoup)

        # content = newSoup.select('div[id="article_page"]')[0].text.replace('\n','')
        # print(content)
        try:
            content1 = newSoup.select('div[id="article_page"]')[0].text.split('走路走錯，日走萬步也傷身，早安健康新刊【走路治病7堂課】雙11特價買1送1，早安會員結帳輸入序號【EDH11】再折111 >>>')[0].replace('\n','')
            content2 = newSoup.select('div[id="article_page"]')[0].text.split('走路走錯，日走萬步也傷身，早安健康新刊【走路治病7堂課】雙11特價買1送1，早安會員結帳輸入序號【EDH11】再折111 >>>')[1].replace('\n','')
            contents = content1 + content2
        except:
            contents = newSoup.select('div[id="article_page"]')[0].text.replace('\n', '')

        # print(name)
        print(contents)
        # print("=============")


        with open("./food_med/{}.txt".format(idNo), "w", encoding="utf-8") as f:
            f.write(contents)



    page += 1
    print('=next page=')