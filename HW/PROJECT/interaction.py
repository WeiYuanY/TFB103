import requests
from bs4 import BeautifulSoup
import json
import os

if not os.path.exists('./InteractionId_1'):
    os.mkdir("./InteractionId_1")

url = "https://go.drugbank.com/drugs?page={}"


userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
headers = {
"User-Agent": userAgent ,"Referer" : "referer: https://go.drugbank.com/drugs"
}



page = 1
for i in range(1,110):
    res = requests.get(url.format(page),headers=headers)
    # print(res.text)
    soup = BeautifulSoup(res.text,'html.parser')
    # print(soup)

    drugs = soup.select('tbody')[0]
    # print(drugs)

    for drugSoup in drugs:
        drugGenericName = drugSoup.select('a')[0].text
        id = drugSoup.select('a')[0]['href'].split('/')[-1]
        Url = 'https://go.drugbank.com/drugs/' + id

        data = ""
        data = "id: " + id + '\n'
        data += "藥名: " + drugGenericName + '\n'
        # data += "網址: " + Url + '\n'



        newUrl = "https://go.drugbank.com/drugs/{}/drug_interactions.json?group=approved&draw={}&start={}&length=100&search"
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        newHeaders = {"User-Agent": userAgent, "Referer": f"referer: https://go.drugbank.com/drugs/{id}"}

        draw = 2
        start = 0
        for r in range(0, 10):
            newRes = requests.get(newUrl.format(id, draw, start), headers=newHeaders)
            # print(newRes.text)
            jsonData = newRes.json()['data']
            # print(jsonData)
            # print(len(jsonData))
            for i in range(len(jsonData)):
                drugNameId = jsonData[i][0].split("drugs/")[1].split('">')[0]
                drugName = jsonData[i][0].split(">")[1].split("<")[0]
                interaction = jsonData[i][1]

                data += "相互作用藥名ID: " + drugNameId + '\n'
                data += "相互作用藥名: " + drugName + '\n'
                data += "相互作用: " + interaction + '\n'
                # print(drugNameId)

            draw += 2
            start += 100

        with open("./InteractionId_1/{}.txt".format(id), "w", encoding="utf-8") as f:
            f.write(data)
        print(data)

    page += 1
    print('===========')