from datetime import time,datetime,timedelta
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

# driver = webdriver.PhantomJS()
# csvFile = open("/home/ham/Envs/scrapy/naverNews.csv", 'wt', newline='', encoding='utf-8')
# writer = csv.writer(csvFile)
# csvRow = []

def getDate():
    startDate = input("Start Date(yyyy,m,d): ")
    endDate = input("End Date(yyyy,m,d): ")
    date1 = datetime.strptime(startDate, "%Y,%m,%d")
    date2 = datetime.strptime(endDate, "%Y,%m,%d")
    delta = date2 - date1         # timedelta
    datesSet = []
    for i in range(delta.days + 1):
        rawDates = date1 + timedelta(days=i)
        newsDates = str(rawDates).replace("00:00:00", "").rstrip()
        datesSet.append(newsDates)
    return datesSet


def scrapeNews():
    datesList = getDate()
    # driver = webdriver.PhantomJS()
    # csvFile = open("/home/ham/Envs/scrapy/naverNews.csv", 'wt', newline='', encoding='utf-8')
    # writer = csv.writer(csvFile)
    csvRow = []
    for i in datesList:
        urls = ["http://news.naver.com/main/history/mainnews/list.nhn?date=%s" % i]
    for url in urls:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        scrap = soup.select('ul.mlist2 > li')
# get Max Number of pages at current page
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
            #    writer.writerow(csvRow)
# get next page
            driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
            driver.implicitly_wait(10)
            #time.sleep(5)
            driver.page_source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            scrap = soup.select('ul.mlist2 > li')
    return csvRow
