"""coded by Ham."""
# csv file name
# remove None from dictionary
# remove func first line of calling class instance
# merge_two Csv files with pandas
# remove duplicated item in csvs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import WebDriverException
import csv
import pandas as pd
import time
import pymysql
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from itertools import zip_longest
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
        print(datetime.now())
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
                time.sleep(2)
        driver.quit()
        return self.wholeHTML

    # making local html file for selenium page loading
    def saveTo_localHtml(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_webpage.html" % (n, n1)
        with open(tmpFile, 'wt', encoding='utf-8') as htmlFile:
            htmlFile.write('<meta charset="utf-8">')
            for html2 in self.wholeHTML:
                htmlFile.write(html2)
        print(datetime.now())
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

    # scrape whole News and saveCsv with line by line using Selenium
    def scrape_wholeNews_saveCsv_bySelenium(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_merged.csv" % (n, n1)
        csvFile = open(tmpFile, 'w', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showtime', 'newsText'])
        self.linkFile = input("upload link file:")
        driver = webdriver.PhantomJS()
        #driver = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')
        driver.get(self.linkFile)
        window_before = driver.window_handles[0]
        newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
        #showtimes = driver.find_elements_by_class_name('eh_edittime')
        showtimes = driver.find_elements_by_class_name('mlist2_info')
        i = 0
        for pageId in range(len(newsLinks)):
            print("pageId processing")
            self.textRow = []
            self.textRow.append([newsLinks[i].text.strip()])
            self.textRow.append([sources[i].text.strip()])
            self.textRow.append([showtimes[i].text.strip()])
            newsLinks[i].click()
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
            newstextID = driver.find_element_by_id('articleBodyContents')
            newsText = newstextID.get_attribute('innerText')
            self.textRow.append([newsText.replace('\n\n', '').strip()])
            writer.writerow(self.textRow)
            print(self.textRow)
            i = i+1
            driver.close()
            driver.switch_to_window(window_before)
        csvFile.close()
        return self.textRow

    # ver.0.8 scrape the whole news save Csv
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
                    newstitles[i].click()
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

    # scrape title, source, showtime of newses using BeautifulSoup
    def scrape_newsLine_bySoup(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_merged.csv" % (n, n1)
        csvFile = open(tmpFile, 'w', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showtime', 'showtime1', 'showtime2', 'newsText'])
        for html in self.wholeHTML:
            print("scrape_newsLine with Beautifulsoup self.wholeHTML processing")
            soup = BeautifulSoup(html, 'html.parser')
            scrap = soup.select('ul.mlist2 > li')
            for item in scrap:
                self.textRow = []
                newstitle = item.find('a')
                self.textRow.append([newstitle.text.strip()])
                source = item.find(attrs={'class': 'writing'})
                self.textRow.append([source.text.strip()])
                showtime = item.findAll(attrs={'class': 'eh_edittime'})
                for sh in showtime:
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
            newstextID = driver.find_element_by_id('articleBodyContents')
            newsText = newstextID.get_attribute('innerText')
            self.textRow5.append([newsText.replace('\n\n', '').strip()])
            driver.close()
            driver.switch_to_window(window_before)
        return self.textRow5

    # scrape the title, source, showtime, news text and return each only list
    def scrape_WholeNews_list(self):
        print(datetime.now())
        linkFile = input("upload link file:")
        driver = webdriver.PhantomJS()
        driver.get(linkFile)
        window_before = driver.window_handles[0]
        newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        self.textRow = [[newstitle.text.strip()] for newstitle in newsLinks]
        sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
        self.textRow1 = [[source.text.strip()] for source in sources]
        showtimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(3)')
        self.textRow2 = [[showtime.text.strip()] for showtime in showtimes]
        print(datetime.now())
        self.textRow5 = []
        for link in newsLinks:
            print("link Processing")
            link.click()
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
            newstextID = driver.find_element_by_id('articleBodyContents')
            newsText = newstextID.get_attribute('innerText')
            self.textRow5.append([newsText.replace('\n\n', '').strip()])
            driver.close()
            driver.switch_to_window(window_before)
        print(datetime.now())
        driver.quit()
        return self.textRow, self.textRow1, self.textRow2, self.textRow5

    def saveTo_CsvFile(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_newstext.csv" % (n, n1)
        with open(tmpFile, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            for i in self.textRow5:
                writer.writerow(i)
        csvFile.close()
        return

    # merge all lists and save to Csv
    def merge_lists_saveCsv(self):
        print(datetime.now())
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_newstext.csv" % (n, n1)
        csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showtime', 'newsText'])
        for i in zip_longest(self.textRow, self.textRow1, self.textRow2, self.textRow5, fillvalue='_'):
            writer.writerow(i)
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

if __name__ == '__main__':
        # print ('starting crawl.py...')
        a = News_crawl()
        print ('getting dates...')
        a.getDate()
        print ('getting urls...')
        a.getUrls()
        a.get_wholeHtml()
        a.saveTo_localHtml()
        a.scrape_wholeNews_saveCsv_bySelenium()
        a.scrape_saveCsv()
        a.scrape_newsLine_bySoup()
        a.scrape_newsText_bySelenium()
        a.scrape_WholeNews_list()
        a.saveTo_CsvFile()
        a.merge_lists_saveCsv()
        a.duplicateItemRemove()
        a.csvToDic()
        a.dicToMysql()
