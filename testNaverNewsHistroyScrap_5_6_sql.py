
from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup
from datetime import date, timedelta
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='ham', passwd='5864', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scraping")
cur.execute("ALTER DATABASE scraping CHARACTER SET utf8 COLLATE utf8_general_ci")
cur.execute("ALTER TABLE pages CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")

driver = webdriver.PhantomJS()
csvFile = open("/home/ham/Envs/scrapy/naverNews.csv", 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
csvRow = []

d1 = date(2017, 4, 1)  # start date
d2 = date(2017, 4, 2)  # end date
delta = d2 - d1         # timedelta
for i in range(delta.days + 1):
    rawDates = d1 + timedelta(days=i)
    newsDates = [str(rawDates)]
    for i in newsDates:
        urls = ["http://news.naver.com/main/history/mainnews/list.nhn?date=%s" % i]
    for url in urls:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        scrap = soup.select('ul.mlist2 > li')
        exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
        splitNum = exmaxNum.split('/')
        maxNum = int(splitNum[1])

        for pageId in range(maxNum):
            for item in scrap:
                csvRow = []
                for news in item.findAll(['a']):
                    csvRow.append(news.get_text().strip())
                for source in item.findAll(attrs={'class': 'writing'}):
                    csvRow.append(source.get_text().strip())
                for showTime in item.findAll(attrs={'class': 'eh_edittime'}):
                    csvRow.append(showTime.get_text().strip())

                insert_stmt = (
                  "INSERT INTO pages (news, source, showtime)"
                  "VALUES (%s, %s, %s)"
                )
                data = (news.get_text().strip(), source.get_text().strip(), showTime.get_text().strip())
                cur.execute(insert_stmt, data)
                writer.writerow(csvRow)

            driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
            #driver.implicitly_wait(5)
            time.sleep(5)
            driver.page_source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            scrap = soup.select('ul.mlist2 > li')

cur.connection.commit()
cur.close()
conn.close()

driver.quit()
csvFile.close()

"""
from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup

url = 'http://news.naver.com/main/history/mainnews/list.nhn'
driver = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
scrap = soup.select('div.mtype_list_wide > ul.mlist2 > li')
csvFile = open("/home/ham/Envs/scrapy/naverNews.csv", 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)

exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
splitNum = exmaxNum.split('/')
maxNum = int(splitNum[1])
print(maxNum)

for pageId in range(1,maxNum):
for item in scrap:
    csvRow = []
    for news in item.findAll(["a","span"]):
        csvRow.append(news.get_text())
    writer.writerow(csvRow)

driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
scrap = soup.select('div.mtype_list_wide > ul.mlist2 > li')
driver.implicitly_wait(7)


csvFile.close()







exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
splitNum = exmaxNum.split('/')
maxNum = int(splitNum[1])

for pageId in range(1,maxNum):


for pageId in range(1,maxNum):
for item in scrap:
    csvRow = []
    for news in item.findAll(["a","span"]):
        csvRow.append(news.get_text())
    writer.writerow(csvRow)
try:
    driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
    time.sleep(2)

except:
    break

csvFile.close()


driver.find_element_by_link_text(str(pageId)).click()
maxNumOfPages = 10; # for example
for pageId in range(2,maxNumOfPages+2):


finally:
csvFile.close()




MULTIPAGE

from selenium.webdriver.firefox import webdriver

driver = webdriver.WebDriver()
driver.get('http://www.walmart.com/ip/29701960?page=seeAllReviews')

maxNumOfPages = 10; # for example
for pageId in range(2,maxNumOfPages+2):
for review in driver.find_elements_by_class_name('BVRRReviewDisplayStyle3Main'):
    title  = review.find_element_by_class_name('BVRRReviewTitle').text
    rating = review.find_element_by_xpath('.//div[@class="BVRRRatingNormalImage"]//img').get_attribute('title')
    print title,rating
try:
    driver.find_element_by_link_text(str(pageId)).click()
except:
    break

driver.quit()



try:
for item in scrap:
    csvRow = []
    for news in item.findAll(["a","span"]):
        csvRow.append(news.get_text())
        writer.writerow(csvRow)
        time.sleep(2)

        for i in range(1,6):
            next_link = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]')
            next_link.click()
            time.sleep(2)

finally:
csvFile.close()


try:
for item in scrap:
    csvRow = []
    for news in item.findAll(["a","span"]):
        csvRow.append(news.get_text())
        writer.writerow(csvRow)
        time.sleep(2)
        next_link = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]')
        next_link.click()
        time.sleep(2)

finally:
    csvFile.close()


#scrapTocsv(scrap)
def scrapTocsv(scrap):
try:
    for item in scrap:
        csvRow = []
        for news in item.findAll(["a","span"]):
            csvRow.append(news.get_text())
        writer.writerow(csvRow)
        time.sleep(2)
        for i in range(1, 3):
            next_link = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]')
            next_link.click()
            time.sleep(2)

finally:
    csvFile.close()


scrapTocsv(scrap)

#for i in range(1,3):
#while True:
scrapTocsv(scrap)
next_link = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]')
next_link.click()
time.sleep(2)

while True:
scrapTocsv(scrap)
next_link = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]')
next_link.click()
time.sleep(2)
#current_page_num = soup.find('div.h.m.text > div.eh_navi > div.eh_page > em')
#get_page_num = soup.find('div.h.m.text > div.eh_navi > div.eh_page')
#c = current_page_num.text.strip()
#g = get_page_num.text.strip()
#if int(c) == int(g):


try:
for item in scrap:
    csvRow = []
    for news in item.findAll(["a","span"]):
        csvRow.append(news.get_text())
    writer.writerow(csvRow)
finally:
csvFile.close()




def scrapTocsv(scrap):
#    for item in scrap.xpath('//*[@id="h.m.text"]/ul'):
for item in scrap:
    news = item.get_text().strip()
    csvFile = open("/home/ham/Envs/scrapy/naverNews.csv", 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
#    try:
#        for item in scrap:
    csvRow = []
    csvRow.append(news)
    writer.writerow(csvRow)
    csvFile.close()


scrapTocsv(scrap)

while True:
scrapTocsv(scrap)
next_link = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]')
next_link.click()
time.sleep(2)
#current_page_num = soup.find('div.h.m.text > div.eh_navi > div.eh_page > em')
#get_page_num = soup.find('div.h.m.text > div.eh_navi > div.eh_page')
#c = current_page_num.text.strip()
#g = get_page_num.text.strip()
#if int(c) == int(g):
"""
