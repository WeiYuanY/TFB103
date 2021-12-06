import time
import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('./food_med_2'):
 os.mkdir("./food_med_2")

url = 'https://health.tvbs.com.tw/search/高血壓/articles/{}'
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
headers = { "User-Agent" : userAgent ,"Referer" : 'https://health.tvbs.com.tw/'}

page = 1
for i in range(1,48):
    res = requests.get(url.format(page), headers = headers)
    soup =BeautifulSoup (res.text, 'html.parser')
    ids = soup.select('div[class="list"]')[1:]

    # #取各篇文章之ID
    for id in ids:
        idNo = id.select('a')[0:19]#濾掉後面的廣告文章
        for i in range(len(idNo)):
            idNos = idNo[i]['href'].split('.tw/')[-1]
            filenames = idNos.replace('/','_')
            idNoss = idNos.split('/')[-1]
            #進入每個ID取出文章內容
            newUrl = f'https://health.tvbs.com.tw/{idNos}'
            newRes = requests.get(newUrl,headers=headers)
            newSoup = BeautifulSoup(newRes.text,"html.parser")

            content = newSoup.select('div[class="detail_div"]')[0].text.replace('\n','').split('◎ 圖片來源')[0]

            #將文章存存成文字檔
            with open("./food_med_2/{}.txt".format(filenames), "w", encoding="utf-8") as f:
                f.write(content)


        page += 1
        time.sleep(2)
