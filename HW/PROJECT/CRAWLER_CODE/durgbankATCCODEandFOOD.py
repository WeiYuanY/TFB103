from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import os
import re



if not os.path.exists('./food1'):
    os.mkdir("./food1")

if not os.path.exists('./drugbankNew'):
    os.mkdir("./drugbankNew")


url = "https://go.drugbank.com/drugs?page={}"


userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
headers = {
"User-Agent": userAgent ,"Referer" : "referer: https://go.drugbank.com/drugs"
}


page = 1
for i in range(1,110):
    res = requests.get(url.format(page),headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    drugs = soup.select('tbody')[0]


    for drugSoup in drugs:
        drugGenericName = drugSoup.select('a')[0].text
        id = drugSoup.select('a')[0]['href'].split('/')[-1]

        newUrl = f"https://go.drugbank.com/drugs/{id}"
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        newHeaders = {"User-Agent": userAgent, "Referer": f"referer: https://go.drugbank.com/drugs/{id}"}

        driver = Chrome()
        driver.get(newUrl.format(id))
        time.sleep(3)

        a = driver.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div[2]/h2[4]').text
        if a == 'PRODUCTS':
            try:
                forms2 = driver.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div[2]/dl[5]').text
            except:
                pass
        else:
            try:
                forms2 = driver.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div[2]/dl[4]').text
            except:
                pass


        try:
            atcCodes = re.findall("[A-Z][0-9]{2}[A-Z]{2}[0-9]{2}",forms2)
            atcCodes = str(atcCodes).replace("[", "").replace("]", "").replace("'", "")
        except:
            atcCodes = str(atcCodes).replace("[", "").replace("]", "").replace("'", "")


        #foodInteractions
        try:
            foodInteractions = driver.find_element(By.XPATH,'//*[@id="food-interactions"]').text
        except:
            pass

        try:
            foodInteractionsC = driver.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div[2]/dl[3]/dd[2]').text
        except:
            pass


        foodData = ''
        foodData += 'Name: ' + drugGenericName + "\n**"
        foodData += 'DrugBankId: ' + id + "\n**"
        foodData += 'ATCCode: ' + atcCodes + "\n**"
        foodData += 'FoodInteractions: ' + foodInteractionsC


        dataNew = ""
        dataNew += 'Name: ' + drugGenericName + "\n"
        dataNew += 'DrugBankId: ' + id + "\n"
        dataNew += 'ATCCode: ' + atcCodes



        with open("./food1/{}.txt".format(id), "w", encoding="utf-8") as f:
            f.write(foodData)

        with open("./drugbankNew/{}.txt".format(id), "w", encoding="utf-8") as f:
            f.write(dataNew)

    page += 1
