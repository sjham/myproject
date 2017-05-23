"""coded by Ham."""

from selenium import webdriver
import csv
import time
import pymysql
from bs4 import BeautifulSoup
from datetime import timedelta, datetime


class News_crawl():
    def __init__(self):

        # self.startDate = input("Start Date(yyyy,m,d): ")
        # self.endDate = input("End Date(yyyy,m,d): ")
        # self.datesSet = datesSet
        # self.urls = urls
        # self.dataRaw = dataRaw
        # # urls = self.urls
        print("Start Crawler")

    def getDate(self):
        # startDate = input("Start Date(yyyy,m,d): ")
        # endDate = input("End Date(yyyy,m,d): ")
        startDate = "2017,5,20"
        endDate = "2017,5,21"
        date1 = datetime.strptime(startDate, "%Y,%m,%d")
        date2 = datetime.strptime(endDate, "%Y,%m,%d")
        delta = date2 - date1         # timedelta
        self.datesSet = []
        for i in range(delta.days + 1):
            rawDates = date1 + timedelta(days=i)
            #yield str(rawDates).replace("00:00:00", "").rstrip()
            newsDates = str(rawDates).replace("00:00:00", "").rstrip()
            self.datesSet.append(newsDates)
        return(self.datesSet)

# a = News_scrawl()
# r = a.getDate()
# for i in r:
#     print(i)
# print(a.datesSet)
#
    def getUrls(self):
        News_crawl.getDate(self)
        self.urls = []
        for i in self.datesSet:
            self.urls.append("http://news.naver.com/main/history/mainnews/list.nhn?date=%s" % i)
        return self.urls

#
# a = News_scrawl()
# a.getUrls()
# print(a.urls)
#
    def scrapeNews(self):
        News_crawl.getUrls(self)
        driver = webdriver.PhantomJS()
        with open("/home/ham/Envs/scrapy/naverNews1.csv", 'wt', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['news', 'source', 'showtime']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader()
        # csvFile = open("/home/ham/Envs/scrapy/naverNews1.csv", 'wt', newline='', encoding='utf-8')
        # writer = csv.writer(csvFile)
        # self.dataRow = []
        for url in self.urls:
            #self.dataRow1 = []
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            scrap = soup.select('ul.mlist2 > li')
            exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
            splitNum = exmaxNum.split('/')
            maxNum = int(splitNum[1])

            for pageId in range(maxNum):
                #self.dataRow1 = []
                for item in scrap:
                    #self.dataRow = []
                    #self.dataRow =
                    writer.writeheader()
                    for self.news in item.findAll(['a']):
                        writer.writerow({'news': self.news.get_text().strip()})
                        # self.dataRow.append(self.news.get_text().strip())
                    for self.source in item.findAll(attrs={'class': 'writing'}):
                        writer.writerow({'source': self.source.get_text().strip()})
                        # self.dataRow.append(self.source.get_text().strip())
                    for self.showTime in item.findAll(attrs={'class': 'eh_edittime'}):
                        writer.writerow({'showtime': self.showtime.get_text().strip()})
                        #self.dataRow.append(self.showTime.get_text().strip())
                    #writer.writerow(self.dataRow)
                    #self.dataRow1.append(self.dataRow)

                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                #driver.implicitly_wait(5)
                time.sleep(5)
                driver.page_source
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                scrap = soup.select('ul.mlist2 > li')

        driver.quit()
        return


a = News_crawl()
a.scrapeNews()
#
# print(a.dataRow)

#
# for i in a.dataRow:
#     print(i)
# #     self.dataRow1.append(i)

#print(t)

#print(a.dataRow1)
# for i in a.dataRow:
#     print(i)


        #self.dataRow1 = []
        # for i in self.dataRow:
        #     self.dataRow1.append(i)
        # return self.dataRow1
#
#     def saveData(self):
#         News_crawl.scrapeNews(self)
#         with open("/home/ham/Envs/scrapy/naverNews.csv", 'w', newline='', encoding='utf-8') as csvFile:
#             self.writer = csv.writer(csvFile)
#             for i in self.scrapeNews.dataRow:
#                 self.writer.writerow(i)
#
#
# a = News_crawl()
# a.saveData()
#print(a.dataRow)


        # self.dataRow1 = list(self.dataRow)
        # return self.dataRow1
#
#
# a = News_crawl()
# t = a.scrapeNews()
# for i in t:
#     print(i)
# print(a.datesSet)

#
# a = News_crawl()
# a.scrapeNews()
# print(a.dataRow1)
# # #
#


            # fieldnames = ['first_name', 'last_name']
            # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #
            # for i in tmp:
            #     i.split(',')
            #     news = i[0]
            #     source = i[1]
            #     showtime = i[2]
            #     conn = pymysql.connect(host='127.0.0.1', user='ham', passwd='5864', db='mysql', charset='utf8')
            #     cur = conn.cursor()
            #     cur.execute("USE scraping")
            #     cur.execute("ALTER DATABASE scraping CHARACTER SET utf8 COLLATE utf8_general_ci")
            #     cur.execute("ALTER TABLE pages CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")
            #
            #     insert_stmt = (
            #       "INSERT INTO pages (news, source, showtime)"
            #       "VALUES (%s, %s, %s)"
            #     )
            #     #data = (self.news.get_text().strip(), self.source.get_text().strip(), self.showTime.get_text().strip())
            #     data = (news, self.source.get_text().strip(, self.showTime.get_text().strip())
            #
            #     cur.execute(insert_stmt, data)
            #     cur.connection.commit()
            #     cur.close()
            #     conn.close()
            #
            #
            #
            #
            #
            # writer.writerow(self.dataRow)
            # # save to MYSQL
            # conn = pymysql.connect(host='127.0.0.1', user='ham', passwd='5864', db='mysql', charset='utf8')
            # cur = conn.cursor()
            # cur.execute("USE scraping")
            # cur.execute("ALTER DATABASE scraping CHARACTER SET utf8 COLLATE utf8_general_ci")
            # cur.execute("ALTER TABLE pages CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")
            #
            # insert_stmt = (
            #   "INSERT INTO pages (news, source, showtime)"
            #   "VALUES (%s, %s, %s)"
            # )
            # data = (self.news.get_text().strip(), self.source.get_text().strip(), self.showTime.get_text().strip())
            # cur.execute(insert_stmt, data)
            # cur.connection.commit()
            # cur.close()
            # conn.close()
            #

#
# obj = News_scrawl()
# obj.getDate()
# #obj.saveData()
# obj.getUrls()
# obj.scrapeNews()
# #getDate
#
# #print(obj.getUrls)
# print(obj.urls)
# print(obj.dataRow)

    # def saveData(self):
    #     # save to CSV
    #     with open("/home/ham/Envs/scrapy/naverNews.csv", 'wt', newline='', encoding='utf-8') as csvFile:
    #         writer = csv.writer(csvFile)
    #         writer.writerow(self.dataRow)
    #         # save to MYSQL
    #         conn = pymysql.connect(host='127.0.0.1', user='ham', passwd='5864', db='mysql', charset='utf8')
    #         cur = conn.cursor()
    #         cur.execute("USE scraping")
    #         cur.execute("ALTER DATABASE scraping CHARACTER SET utf8 COLLATE utf8_general_ci")
    #         cur.execute("ALTER TABLE pages CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")
    #
    #         insert_stmt = (
    #           "INSERT INTO pages (news, source, showtime)"
    #           "VALUES (%s, %s, %s)"
    #         )
    #         data = (self.news.get_text().strip(), self.source.get_text().strip(), self.showTime.get_text().strip())
    #         cur.execute(insert_stmt, data)
    #         cur.connection.commit()
    #         cur.close()
    #         conn.close()
    #
    #
    #

#
# obj = News_scrawl()
# obj.getDate()
# print(obj.datesSet)
#

    # save to MYSQL
    # insert_stmt = (
    #   "INSERT INTO pages (news, source, showtime)"
    #   "VALUES (%s, %s, %s)"
    # )
    # data = (news.get_text().strip(), source.get_text().strip(), showTime.get_text().strip())
    # cur.execute(insert_stmt, data)
    # cur.connection.commit()
    # cur.close()
    # conn.close()
# obj = News_scrawl()
# obj.getDate()
# obj.getUrls

# #
# if __name__ == '__main__':
#     getDate()
#


#
# if __name__ == '__main__':
#     a = NewsScrape('2017,4,1','2017,4,2','http://news.naver.com/main/history/mainnews/list.nhn')
#     a.getDate()
