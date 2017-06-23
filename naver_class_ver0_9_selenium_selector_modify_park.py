"""coded by Ham."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd
import time
import pymysql
#from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from itertools import zip_longest
#import progressbar


class News_crawl():
    def __init__(self):
        print("Start Crawler")

    def getDate(self):
        self.startDate = input("Start Date(yyyy,m,d): ")
        self.endDate = input("End Date(yyyy,m,d): ")
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

    def scrape_saveCsv(self):
        driver = webdriver.PhantomJS()
        #driver = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s.csv" % (n, n1)
        csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['news', 'source', 'showtime','newstext'])

        for url in self.urls:
            print("url processing")
            driver.get(url)
            # html = driver.page_source
            # soup = BeautifulSoup(html, 'html.parser')
            # scrap = soup.select('ul.mlist2 > li')
            window_before = driver.window_handles[0]
            exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
            splitNum = exmaxNum.split('/')
            self.maxNum = int(splitNum[1])
            print(self.maxNum)

            for pageId in range(self.maxNum):
                print("pageId processing")
                i = 0
                for item in range(20):
                    print("item processing")
                    self.dataRow = []
                    newstitles = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
                    self.dataRow.append(newstitles[i].text.strip())
                    sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
                    self.dataRow.append(sources[i].text.strip())
                    showtimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.eh_edittime')
                    self.dataRow.append(showtimes[i].text.strip())

                    newstitles = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
                    newstitles[i].click()
                    #driver.findElement(By.cssSelector("p.product_desc > a")).click();

                    driver.implicitly_wait(10)
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    #driver.implicitly_wait(10)
                    #driver.get(url)
                    WebDriverWait(driver, 20).until(
                         EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
                    #EC.presence_of_all_elements_located())
                    #time.sleep(5)
                    demo_div = driver.find_element_by_id('articleBodyContents')
                    newsText = demo_div.get_attribute('innerText')
                    self.dataRow.append([newsText.replace('\n\n', '').strip()])
                    print(self.dataRow)
                    writer.writerow(self.dataRow)
                    driver.close()
                    driver.switch_to_window(window_before)
                    time.sleep(2)
                    i = i+1

                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                driver.switch_to_window(window_before)
                driver.implicitly_wait(10)
                # html = driver.page_source
                # soup = BeautifulSoup(html, 'html.parser')
                # scrap = soup.select('ul.mlist2 > li')
                # driver.implicitly_wait(10)
                # window_third = driver.window_handles[2]
                # driver.switch_to_window(window_third)
                #time.sleep(5)
        driver.quit()
        csvFile.close()
        return

    def scrape_newsText(self):
        # Scrape title, source, showing time, news text between certain dates.
        # CSV file
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_merged.csv" % (n, n1)
        csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showtime', 'newsText'])

        driver = webdriver.PhantomJS()
        #driver = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')

        for url in self.urls:
            print("url processing")
            driver.get(url)
            window_before = driver.window_handles[0]
            # Get max page number of current url
            exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
            splitNum = exmaxNum.split('/')
            maxNum = int(splitNum[1])
            print(maxNum)
            # Get titles, news texts etc of the current page
            for pageId in range(maxNum):
                print(" pageId processing")
                driver.implicitly_wait(10)
                newstitles = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
                textRow = [[newstitle.text.strip()] for newstitle in newstitles]
                sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
                textRow1 = [[source.text.strip()] for source in sources]
                showtimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.eh_edittime')
                textRow2 = [[showtime.text.strip()] for showtime in showtimes]
                textRow3 = []
                for newstitle in newstitles:
                    print("inner text processing")
                    driver.implicitly_wait(20)
                    newstitle.click()
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    demo_div = driver.find_element_by_id('articleBodyContents')
                    newsText = demo_div.get_attribute('innerText')
                    textRow3.append([newsText.replace('\n\n', '').strip()])
                    driver.close()
                    driver.switch_to_window(window_before)

                # Merge produced list files
                for i in zip_longest(textRow, textRow1, textRow2, textRow3, fillvalue='_'):
                    writer.writerow(i)
                driver.implicitly_wait(20)
                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
        driver.quit()
        csvFile.close()
        return

    def duplicateItemRemove(self):
        dupedCsv = input("Enter the name of file to singlify: ")
        singledCsv = input("Enter the name of file singlified: ")
        with open(dupedCsv, 'r') as in_file, open(singledCsv, 'w') as out_file:
            seen = set() # set for fast O(1) amortized lookup
            for line in in_file:
                if line in seen: continue # skip duplicate
                seen.add(line)
                out_file.write(line)
        return

    def merge_twoCsvs(self):
        firstCsv = input("Enter the name of first file to merge: ")
        secondCsv = input("Enter the name of second file to merge: ")
        test1 = pd.read_csv(firstCsv)
        test2 = pd.read_csv(secondCsv)
        test3 = pd.concat([test1, test2], axis=1)
        test3.to_csv("/home/ham/Envs/scrapy/naverNews_merged.csv")

    def csvToDic(self):
        self.data = []
        with open("/home/ham/Envs/scrapy/naverNews1.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            # next(reader)
            for line in reader:
                for key, value in line.items():
                    if value is None:
                        line[key] = 0
                self.data.append(line)
        return self.data
# a = News_crawl()
# a.csvToDic()
# print(a.data)

    def dicToMysql(self):
        result = News_crawl.csvToDic(self)
        conn = pymysql.connect(host='127.0.0.1', user='ham', passwd='5864', db='mysql', charset='utf8')
        cur = conn.cursor()
        cur.execute("USE scraping")
        #query = "INSERT INTO pages (news, source, showtime, showtime2, showtime3, newstext) VALUES (%s, %s, %s, %s, %s, %s)"
        query = "INSERT INTO pages (news, source, showtime, showtime2, showtime3) VALUES (%s, %s, %s, %s, %s)"

        news_list = [item['news'] for item in result]
        source_list = [item['source'] for item in result]
        showtime_list = [item['showtime'] for item in result]
        showtime2_list = [item['showtime2'] for item in result]
        showtime3_list = [item['showtime3'] for item in result]
        #newstext_list = [item['newstext'] for item in result]
        print(news_list)
        print(source_list)
        print(showtime_list)
        print(showtime2_list)
        print(showtime3_list)
        #print(newstext_list)
        values = (",".join(news_list), ",".join(source_list), ",".join(showtime_list), ",".join(showtime2_list), ",".join(showtime3_list), ",".join(newstext_list))
        #values = (",".join(news_list), ",".join(source_list), ",".join(showtime_list), ",".join(showtime2_list), ",".join(showtime3_list), ",".join(newstext_list))
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()

# a = News_crawl()
# a.dicToMysql()


if __name__ == '__main__':
        # print ('starting crawl.py...')
        a = News_crawl()
        print ('getting dates...')
        # a.startDate = input("Start Date(yyyy,m,d): ")
        # a.endDate = input("End Date(yyyy,m,d): ")
        print ('getting dates...')
        a.getDate()
        print ('getting urls...')
        a.getUrls()
        # print ('scraping and save to Csv file...')
        #a.scrape_saveCsv()
        # print ('converting csv file to dictionary')
        a.scrape_newsText()
        # print ('scraping news Text...')
        #a.duplicateItemRemove()
        #a.merge_twoCsvs()
        # # a.csvToDic()
        # print ('sending dictionay to Mysql..')
        # a.dicToMysql()
