
from selenium import webdriver
import time
import csv
import pymysql
from bs4 import BeautifulSoup
from datetime import timedelta, datetime


class News_scrawl():

    def __init__(self):
        # self.startDate = input("Start Date(yyyy,m,d): ")
        # self.endDate = input("End Date(yyyy,m,d): ")
        # self.datesSet = datesSet
        # self.urls = urls
        # self.dataRaw = dataRaw
        # # urls = self.urls

        print("start")

    def getDate(self):
        # startDate = input("Start Date(yyyy,m,d): ")
        # endDate = input("End Date(yyyy,m,d): ")
        startDate = "2017,4,1"
        endDate = "2017,4,2"
        date1 = datetime.strptime(startDate, "%Y,%m,%d")
        date2 = datetime.strptime(endDate, "%Y,%m,%d")
        delta = date2 - date1         # timedelta
        self.datesSet = []
        for i in range(delta.days + 1):
            rawDates = date1 + timedelta(days=i)
            newsDates = str(rawDates).replace("00:00:00", "").rstrip()
            self.datesSet.append(newsDates)
        return(self.datesSet)
        #print(self.datesSet)


    def getUrls(self):
        News_scrawl.getDate(self)
        self.urls = []
        for i in self.datesSet:
            self.urls.append("http://news.naver.com/main/history/mainnews/list.nhn?date=%s" % i)
        return(self.urls)
        #print(self.urls)


    def scrapeNews(self):
        News_scrawl.getUrls(self)
        driver = webdriver.PhantomJS()
        for url in self.urls:
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            scrap = soup.select('ul.mlist2 > li')
            exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
            splitNum = exmaxNum.split('/')
            maxNum = int(splitNum[1])

            for pageId in range(maxNum):
                self.dataRow = []
                for item in scrap:
                    #self.dataRow = []
                    for self.news in item.findAll(['a']):
                        self.dataRow.append(self.news.get_text().strip())
                    for self.source in item.findAll(attrs={'class': 'writing'}):
                        self.dataRow.append(self.source.get_text().strip())
                    for self.showTime in item.findAll(attrs={'class': 'eh_edittime'}):
                        self.dataRow.append(self.showTime.get_text().strip())
                        #self.dataRow.append('\n')
                    #writer.writerow(self.dataRow)

                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                driver.implicitly_wait(5)
                #time.sleep(5)
                driver.page_source
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                scrap = soup.select('ul.mlist2 > li')
        driver.quit()
        return self.dataRow
        # tmp = str(self.dataRow).split("'\n'")
        # print(tmp[0])
        #print(tmp[1])
        #print(tmp[2])
        #return tmp
    #     tmp = self.dataRow.split('\n')
    def dataTrim(self):
        News_scrawl.scrapeNews(self)
        tmp = self.dataRow
        for i in range(0, len(tmp), 3):
            yield tmp[i:i + 3]

    def saveData(self):
        News_scrawl.dataTrim(self)
        tmp_trim = list(self.dataTrim())
        conn = pymysql.connect(host='127.0.0.1', user='ham', passwd='5864', db='mysql', charset='utf8')
        cur = conn.cursor()
        cur.execute("USE scraping")
        cur.execute("ALTER DATABASE scraping CHARACTER SET utf8 COLLATE utf8_general_ci")
        cur.execute("ALTER TABLE pages CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci")

        insert_stmt = (
          "INSERT INTO pages (news, source, showtime)"
          "VALUES (%s, %s, %s)"
        )
        #data = (self.news.get_text().strip(), self.source.get_text().strip(), self.showTime.get_text().strip())
        data = (tmp_trim[0], tmp_trim[1], tmp_trim[2])

        cur.execute(insert_stmt, data)
        cur.connection.commit()
        cur.close()
        conn.close()
    #
    # #save to CSV
    # with open("/home/ham/Envs/scrapy/naverNews.csv", 'wt', newline='', encoding='utf-8') as csvFile:
    #     writer = csv.writer(csvFile)
    #
    #     for i in tmp:
    #         i.split(',')
    #         news = i[0]
    #         source = i[1]
    #         showtime = i[2]
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
    #         #data = (self.news.get_text().strip(), self.source.get_text().strip(), self.showTime.get_text().strip())
    #         data = (news, source, showtime)
    #
    #         cur.execute(insert_stmt, data)
    #         cur.connection.commit()
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

obj = News_scrawl()
#obj.getDate()
#obj.saveData()
#obj.getUrls()
obj.saveData()
#getDate

#print(obj.getUrls)
#print(obj.urls)
#print(obj.dataRow)


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
