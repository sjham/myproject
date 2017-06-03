"""coded by Ham."""
# csv file name
# remove None from dictionary
# remove func first line of calling class instance
from selenium import webdriver
import csv
import time
import pymysql
#import MySQLdb
from bs4 import BeautifulSoup
from datetime import timedelta, datetime


class News_crawl():
    def __init__(self):
        print("Start Crawler")

    def getDate(self):
        date1 = datetime.strptime(self.startDate, "%Y,%m,%d")
        date2 = datetime.strptime(self.endDate, "%Y,%m,%d")
        delta = date2 - date1
        self.datesSet = []
        for i in range(delta.days + 1):
            rawDates = date1 + timedelta(days=i)
            newsDates = str(rawDates).replace("00:00:00", "").rstrip()
            self.datesSet.append(newsDates)
        return(self.datesSet)


    def getUrls(self):
        self.urls = []
        for i in self.datesSet:
            self.urls.append("http://news.naver.com/main/history/mainnews/list.nhn?date=%s" % i)
        return self.urls


    def scrape_SaveCsv(self):
        driver = webdriver.PhantomJS()
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s.csv" % (n, n1)
        csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['news', 'source', 'showtime', 'showtime2', 'showtime3', 'newstext'])

        for url in self.urls:
            driver.get(url)
            window_before = driver.window_handles[0]

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            scrap = soup.select('ul.mlist2 > li')
            exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
            splitNum = exmaxNum.split('/')
            maxNum = int(splitNum[1])

            for pageId in range(maxNum):
                for item in scrap:
                    self.dataRow = []
                    for self.news in item.findAll(['a']):
                        self.dataRow.append(self.news.get_text().strip())
                    for self.source in item.findAll(attrs={'class': 'writing'}):
                        self.dataRow.append(self.source.get_text().strip())
                    for self.showTime in item.findAll(attrs={'class': 'eh_edittime'}):
                        self.dataRow.append(self.showTime.get_text().strip())
                itemTuples = []
                #dataRow = []
                for i in range(1, 5):
                    for j in range(1, 6):
                        itemTuples.append((i, j))
                print(itemTuples)
                for i in itemTuples:
                    #self.dataRow = []
                    driver.find_element_by_xpath('//*[@id="h.m.text"]/ul[%d]/li[%d]/a' % i).click()
                    #driver.implicitly_wait(3)
                    #time.sleep(5)
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    time.sleep(2)
                    demo_div = driver.find_element_by_id("articleBodyContents")
                    newsText = demo_div.get_attribute('innerText')
                    #time.sleep(5)
                    #driver.implicitly_wait(10)
                    self.dataRow.append([newsText.replace('\n\n', '').strip()])
                    driver.close()
                    driver.switch_to_window(window_before)
                    time.sleep(2)
                    print(self.dataRow)
                    writer.writerow(self.dataRow)
                    #
                    # itemTuples = []
                    # for i in range(1, 5):
                    #     for j in range(1, 6):
                    #         itemTuples.append((i, j))
                    # for i in itemTuples:
                    #     driver.find_element_by_xpath('//*[@id="h.m.text"]/ul[%d]/li[%d]/a' % i).click()
                    #     driver.implicitly_wait(3)
                    #     window_after = driver.window_handles[1]
                    #     driver.switch_to_window(window_after)
                    #     demo_div = driver.find_element_by_id("articleBodyContents")
                    #     newsText = demo_div.get_attribute('innerText')
                    #     #self.dataRow.append(demo_div.get_attribute('innerText'))
                    #     #print(newsText)
                    #     driver.implicitly_wait(10)
                    #     #print(newsText.replace('\n', ''))
                    #     self.dataRow.append(newsText.replace('\n\n', '').strip())
                    #     driver.close()
                    #     driver.switch_to_window(window_before)
                    # #driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                    #time.sleep(5)
                    #writer.writerow(self.dataRow)

                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                time.sleep(5)
                driver.page_source
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                scrap = soup.select('ul.mlist2 > li')
        driver.close()

        csvFile.close()
        return


    def csvToDic(self):
        self.data = []
        with open("/home/ham/Envs/scrapy/naverNews1.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            # next(reader)
            for line in reader:
                for key, value in line.items():
                    if value is None:
                        line[key] = ''
                self.data.append(line)
            # news_list = [item['news'] for item in self.data]
            # source_list = [item['source'] for item in self.data]
            # showtime_list = [item['showtime'] for item in self.data]
            # showtime2_list = [item['showtime2'] for item in self.data]
            # showtime3_list = [item['showtime2'] for item in self.data]

        return self.data
# a = News_crawl()
# a.csvToDic()
# print(a.data)

    def dicToMysql(self):
        result = News_crawl.csvToDic(self)
        conn = pymysql.connect(host='127.0.0.1', user='ham', passwd='5864', db='mysql', charset='utf8')
        cur = conn.cursor()
        cur.execute("USE scraping")
        query = "INSERT INTO pages (news, source, showtime, showtime2, showtime3, newstext) VALUES (%s, %s, %s, %s, %s, %s)"

        news_list = [item['news'] for item in result]
        source_list = [item['source'] for item in result]
        showtime_list = [item['showtime'] for item in result]
        showtime2_list = [item['showtime2'] for item in result]
        showtime3_list = [item['showtime3'] for item in result]
        newstext_list = [item['newstext'] for item in result]
        print(news_list)
        print(source_list)
        print(showtime_list)
        print(showtime2_list)
        print(showtime3_list)
        print(newstext_list)

        values = (",".join(news_list), ",".join(source_list), ",".join(showtime_list), ",".join(showtime2_list), ",".join(showtime3_list), ",".join(newstext_list))
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()

# a = News_crawl()
# a.dicToMysql()


if __name__ == '__main__':
        print ('starting crawl.py...')
        a = News_crawl()
        print ('getting dates...')
        a.startDate = input("Start Date(yyyy,m,d): ")
        a.endDate = input("End Date(yyyy,m,d): ")
        print ('getting dates...')
        a.getDate()
        print ('getting urls...')
        a.getUrls()
        print ('scraping and save to Csv file...')
        a.scrape_SaveCsv()
        print ('converting csv file to dictionary')
        a.csvToDic()
        print ('sending dictionay to Mysql..')
        a.dicToMysql()
