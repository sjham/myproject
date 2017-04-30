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

"""
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