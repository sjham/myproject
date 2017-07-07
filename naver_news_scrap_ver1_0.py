"""written by Ham."""

import os
import csv
import time
import pymysql
#import threading
import pandas as pd
from datetime import timedelta, datetime
from itertools import zip_longest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import WebDriverException
#import progressbar


class News_crawl():
    def __init__(self):
        print("Start Crawler")
        return None
        # bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        # for i in range(20):
        #     time.sleep(0.1)
        #     bar.update(i)

    # get user input dates(from, to) dateset formatted(ex:'2017-3-1')
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
        return self.datesSet

    # making target urls with dates
    def getUrls(self):
        self.urls = []
        for i in self.datesSet:
            self.urls.append("http://news.naver.com/main/history/mainnews/list.nhn?date=%s" % i)
        return self.urls

    # get the whole outerHtmls of multi pages obtained by clicks
    def get_wholeHtml(self):
        print("start get_wholeHtml", datetime.now())
        driver = webdriver.PhantomJS()
        self.wholeHTML = []
        for url in self.urls:
            print("get_wholeHtml url processing")
            driver.get(url)
            exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
            splitNum = exmaxNum.split('/')
            maxNum = int(splitNum[1])
            print(maxNum)
            for pageId in range(maxNum):
                print("get_wholeHtml pageId processing")
                find_div = driver.find_element_by_id('h.m.text')
                newsHtml = find_div.get_attribute('outerHTML')
                self.wholeHTML.append(newsHtml)
                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                time.sleep(1)
        driver.quit()
        return self.wholeHTML

    # making local html file for selenium page loading
    def saveTo_localHtml(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_%s_to_%s_webpage.html" % (n, n1)
        with open(tmpFile, 'wt', encoding='utf-8') as htmlFile:
            htmlFile.write('<meta charset="utf-8">')
            for html2 in self.wholeHTML:
                htmlFile.write(html2)
        #print("end local Html", datetime.now())
        print(self.wholeHTML)
        return

    def get_wholeHtml2(self):
        driver = webdriver.PhantomJS()
        self.wholeHTML = []
        for url in self.urls:
            print("url processing")
            driver.get(url)
            pageSource = driver.page_source
            self.wholeHTML.append(pageSource)
        return self.wholeHTML

    # Main Func. scrape whole News and saveCsv with line by line using Selenium
    def main_scrape_news_saveCsv(self):
        print("start main_scrape_news_saveCsv", datetime.now())
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_%s_to_%s_wholeNews.csv" % (n, n1)
        csvFile = open(tmpFile, 'w', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showTime', 'newsText'])
        self.linkFile = input("upload link file:")
        driver = webdriver.PhantomJS()
        #driver = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')
        driver.get(self.linkFile)
        window_before = driver.window_handles[0]
        newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
        #showTimes = driver.find_elements_by_class_name('eh_edittime')
        showTimes = driver.find_elements_by_class_name('mlist2_info')
        i = 0
        for pageId in range(len(newsLinks)):
            print("pageId processing")
            self.textRow = []
            self.textRow.append([newsLinks[i].text.strip()])
            self.textRow.append([sources[i].text.strip()])
            # self.textRow.append([showTimes[i].text.strip()])
            self.textRow.append([showTimes[i].text.strip().replace(sources[i].text.strip(), '')])
            newsLinks[i].click()
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            time.sleep(1)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
            newsTextID = driver.find_element_by_id('articleBodyContents')
            newsText = newsTextID.get_attribute('innerText')
            self.textRow.append([newsText.replace('\n\n', '').strip()])
            writer.writerow(self.textRow)
            #print(self.textRow)
            i = i+1
            driver.close()
            driver.switch_to_window(window_before)
        csvFile.close()
        #print("end main_scrape_news_saveCsv", datetime.now())
        return self.textRow

    # ver.0.8 main scrape the whole news save Csv
    def scrape_saveCsv(self):
        driver = webdriver.PhantomJS()
        #driver = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_%s_to_%s.csv" % (n, n1)
        csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['news', 'source', 'showTime','newsText'])
        for url in self.urls:
            print("url processing")
            driver.get(url)
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
                    newsTitles = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
                    self.dataRow.append(newsTitles[i].text.strip())
                    sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
                    self.dataRow.append(sources[i].text.strip())
                    showTimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.eh_edittime')
                    self.dataRow.append(showTimes[i].text.strip())
                    newsTitles[i].click()
                    driver.implicitly_wait(10)
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    WebDriverWait(driver, 20).until(
                         EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
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

        driver.quit()
        csvFile.close()
        return

    # scrape title, source, showTime except newstext of newses using BeautifulSoup
    def scrape_newsLine_bySoup(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_%s_to_%s_merged.csv" % (n, n1)
        csvFile = open(tmpFile, 'w', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showTime', 'showTime1', 'showTime2', 'newsText'])
        for html in self.wholeHTML:
            print("scrape_newsLine with Beautifulsoup self.wholeHTML processing")
            soup = BeautifulSoup(html, 'html.parser')
            scrap = soup.select('ul.mlist2 > li')
            for item in scrap:
                self.textRow = []
                newsTitle = item.find('a')
                self.textRow.append([newsTitle.text.strip()])
                source = item.find(attrs={'class': 'writing'})
                self.textRow.append([source.text.strip()])
                showTime = item.findAll(attrs={'class': 'eh_edittime'})
                for sh in showTime:
                    self.textRow.append([sh.text.strip()])
                writer.writerow(self.textRow)
        return self.textRow

    # scrape only texts of each news through click
    def scrape_newsText_bySelenium(self):
        driver = webdriver.PhantomJS()
        driver.get(self.linkFile)
        window_before = driver.window_handles[0]
        newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        self.textRow5 = []
        for link in newsLinks:
            print("link Processing")
            link.click()
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
            newsTextID = driver.find_element_by_id('articleBodyContents')
            newsText = newsTextID.get_attribute('innerText')
            self.textRow5.append([newsText.replace('\n\n', '').strip()])
            driver.close()
            driver.switch_to_window(window_before)
        return self.textRow5

    # save news texts list to Csv
    def saveTo_CsvFile(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_%s_to_%s_newsText.csv" % (n, n1)
        with open(tmpFile, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            for i in self.textRow5:
                writer.writerow(i)
        csvFile.close()
        return

    # scrape the title, source, showTime, news text and return each only list type
    def scrape_WholeNews_list(self):
        print(datetime.now())
        linkFile = input("upload link file:")
        driver = webdriver.PhantomJS()
        driver.get(linkFile)
        window_before = driver.window_handles[0]
        newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        self.textRow = [[newsTitle.text.strip()] for newsTitle in newsLinks]
        sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
        self.textRow1 = [[source.text.strip()] for source in sources]
        showTimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(3)')
        self.textRow2 = [[showTime.text.strip()] for showTime in showTimes]
        print(datetime.now())
        self.textRow5 = []
        for link in newsLinks:
            print("link Processing")
            link.click()
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
            newsTextID = driver.find_element_by_id('articleBodyContents')
            newsText = newsTextID.get_attribute('innerText')
            self.textRow5.append([newsText.replace('\n\n', '').strip()])
            driver.close()
            driver.switch_to_window(window_before)
        print(datetime.now())
        driver.quit()
        return self.textRow, self.textRow1, self.textRow2, self.textRow5

    # merge all lists and save to Csv
    def merge_lists_saveCsv(self):
        print(datetime.now())
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/navernews/naverNews_%s_to_%s_newsText.csv" % (n, n1)
        csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showTime', 'newsText'])
        for i in zip_longest(self.textRow, self.textRow1, self.textRow2, self.textRow5, fillvalue='_'):
            writer.writerow(i)
        return

    def duplicatedItem_remove(self):
        dupedCsv = input("Enter the name of file to singlify: ")
        singledCsv = input("Enter the name of file singlified: ")
        with open(dupedCsv, 'r') as in_file, open(singledCsv, 'w') as out_file:
            seen = set()
            for line in in_file:
                if line in seen: continue
                seen.add(line)
                out_file.write(line)
        return

    def merge_twoCsvs(self):
        firstCsv = input("Enter the name of first file to merge: ")
        secondCsv = input("Enter the name of second file to merge: ")
        test1 = pd.read_csv(firstCsv)
        test2 = pd.read_csv(secondCsv)
        test3 = pd.concat([test1, test2], axis=1)
        test3.to_csv("/home/ham/Envs/scrapy/navernews/naverNews_merged.csv")

    def csvToDic_oneFile(self):
        csvdata = input("upload csv file:")
        self.data = []
        with open("/home/ham/Envs/scrapy/navernews/"+csvdata) as csvfile:
            reader = csv.DictReader(csvfile)
            # next(reader)
            for line in reader:
                for key, value in line.items():
                    if value is None:
                        line[key] = 0
                self.data.append(line)
        return self.data

    def csvToDic_allFiles(self):
        self.alldata = []
        for file in os.listdir("/home/ham/Envs/scrapy/navernews"):
            if file.endswith(".csv"):
                fileList = os.path.join("/home/ham/Envs/scrapy/navernews", file)
        for list in fileList:
            with open("/home/ham/Envs/scrapy/navernews/naverNews1.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                # next(reader)
                for line in reader:
                    for key, value in line.items():
                        if value is None:
                            line[key] = 0
                    self.alldata.append(line)
        return self.alldata

    def dicToMysql(self):
        #result = News_crawl.csvToDic(self)
        conn = pymysql.connect(host='127.0.0.1', user='ham', passwd='5864', db='mysql', charset='utf8')
        cur = conn.cursor()
        cur.execute("USE scraping")
        #query = "INSERT INTO pages (news, source, showTime, showTime2, showTime3, newsText) VALUES (%s, %s, %s, %s, %s, %s)"
        query = "INSERT INTO pages (newsTitle, source, showTime, newsText) VALUES (%s, %s, %s, %s)"

        newsTitle_list = [item['newsTitle'] for item in self.data]
        source_list = [item['source'] for item in self.data]
        showTime_list = [item['showTime'] for item in self.data]
        # showTime2_list = [item['showTime2'] for item in self.data]
        # showTime3_list = [item['showTime3'] for item in self.data]
        newsText_list = [item['newsText'] for item in self.data]
        print(newsTitle_list)
        print(source_list)
        print(showTime_list)
        # print(showTime2_list)
        # print(showTime3_list)
        print(newsText_list)
        values = (",".join(newsTitle_list), ",".join(source_list), ",".join(showTime_list), ",".join(newsText_list))
        #values = (",".join(news_list), ",".join(source_list), ",".join(showTime_list), ",".join(showTime2_list), ",".join(showTime3_list), ",".join(newsText_list))
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()

if __name__ == '__main__':
        # print ('starting crawl.py...')
        a = News_crawl()
        print ('getting dates...')
        a.getDate()
        # # print ('getting urls...')
        a.getUrls()
        a.get_wholeHtml()
        a.saveTo_localHtml()
        a.main_scrape_news_saveCsv()
        # a.scrape_saveCsv()
        # a.scrape_newsLine_bySoup()
        # a.scrape_newsText_bySelenium()
        # a.scrape_WholeNews_list()
        # a.saveTo_CsvFile()
        # a.merge_lists_saveCsv()
        # a.duplicatedItem_remove()
        # a.csvToDic_oneFile()
        # a.dicToMysql()
