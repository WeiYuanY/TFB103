import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('./jobs_104'):
    os.mkdir("./jobs_104")

url = 'https://www.104.com.tw/jobs/search/?keyword={}&page={}'
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

headers = { "User-Agent" : userAgent }
keywords = ['雲端數據分析師','資料科學家']
# keywords = '%20'.join(keywords_list)

page = 1
for i in range(1,10):
    res = requests.get(url.format(keywords,page), headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    jobs = soup.select('div[class="b-block__left"]')[3:]
    # print(jobs)

    # print('===========')
    for jobSoup in jobs:
        job = jobSoup.select('a')[0].text
        company = jobSoup.select('a')[1]['title'].split("\n")[0].split('：')[1]
        address = jobSoup.select('a')[1]['title'].split("\n")[1].split('：')[1]
        industry = jobSoup.select('li')[2].text
        city = jobSoup.select('li')[3].text
        experience = jobSoup.select('li')[4].text
        degree = jobSoup.select('li')[5].text
        jobContent = jobSoup.select('p[class="job-list-item__info b-clearfix b-content"]')[0].text
        jobUrl = 'https:' + jobSoup.select('a')[0]['href']

        # print(job)
        # print(company)
        # print(address)
        # print(industry)
        # print(city)
        # print(experience)
        # print(degree)
        # print(jobContent)
        # print(jobUrl)
        # print('===============')

        openings = ""
        openings += '職稱: ' + job + '\n'
        openings += '公司名稱: ' + company + '\n'
        openings += '地址: ' + address + '\n'
        openings += '產業: ' + industry + '\n'
        openings += '地區: ' + city + '\n'
        openings += '經驗: ' + experience + '\n'
        openings += '學位: ' + degree + '\n'
        # openings += '工作內容: ' + jobContent + '\n'
        openings += '網址: ' + jobUrl


        print(openings)


        try:
            with open("./jobs_104/{}.txt".format(job), "w", encoding="utf-8") as f:
                f.write(openings)
        except FileNotFoundError:
            job = job.replace('/','-')
            with open("./jobs_104/{}.txt".format(job), "w", encoding="utf-8") as f:
                f.write(openings)
        except OSError:
            pass


    page += 1
    print('===========')
