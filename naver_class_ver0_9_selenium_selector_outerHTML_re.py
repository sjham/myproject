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
        #
        # bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        # for i in range(20):
        #     time.sleep(0.1)
        #     bar.update(i)

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
        #i = 0
        #self.dataRow = []
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
                    #showTimelist = []
                    newstitles = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
                    self.dataRow.append(newstitles[i].text.strip())
                    # print(newstitles[0])
                    # print(newstitles[1])
                    #
                    # print(newstitles[2])
                    # print(newstitles[3])

                    sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
                    self.dataRow.append(sources[i].text.strip())
                    showtimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.eh_edittime')
                    self.dataRow.append(showtimes[i].text.strip())
                    # showtimes = driver.find_elements_by_class_name('mlist2_info mlist2_info_multi')
                    # self.dataRow.append(showtimes[i].text.strip())
                    #showtimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.eh_edittime')
                    #
                    # newstitles = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
                    # for newstitle in newstitles:
                    #     textRow.append(newstitle.text.strip())
                    # sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
                    # for source in sources:
                    #     textRow1.append(source.text.strip())
                    # showtimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.eh_edittime')
                    # for showtime in showtimes:
                    #     textRow2.append(showtime.text.strip())
                    # print("item processing")
                    #
                    #
                    # self.dataRow = []
                    # showTimelist = []
                    # self.news = item.find(['a'])
                    # #self.news = driver.find_element_by_css_selector('ul.mlist2 > li > a')
                    # self.dataRow.append(self.news.get_text().strip())
                    # #self.dataRow.append(self.news.text.strip())
                    # self.source = item.find(attrs={'class': 'writing'})
                    # #self.source = driver.find_element_by_class_name('writing')
                    # self.dataRow.append(self.source.get_text().strip())
                    # #self.dataRow.append(self.source.text.strip())
                    # #for self.showTime in driver.find_elements_by_class_name('eh_edittime'):
                    # for self.showTime in item.findAll(attrs={'class': 'eh_edittime'}):
                    #     showTimelist.append(self.showTime.get_text().strip())
                    #     #showTimelist.append(self.showTime.text.strip())
                    # self.dataRow.append(showTimelist)

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
                    # driver.current_url
                    # driver.page_source
                    time.sleep(2)
                    i = i+1
                    #print(self.dataRow)
                    #writer.writerow(self.dataRow)
                #driver.switch_to_window(window_before)

                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                driver.switch_to_window(window_before)
                driver.implicitly_wait(10)
                # html = driver.page_source
                # soup = BeautifulSoup(html, 'html.parser')
                # scrap = soup.select('ul.mlist2 > li')
                #driver.implicitly_wait(10)
                # window_third = driver.window_handles[2]
                # driver.switch_to_window(window_third)

                #time.sleep(5)
        driver.quit()
        csvFile.close()
        return

    def get_wholeHtml(self):
        print(datetime.now())
        driver = webdriver.PhantomJS()
        self.wholeHTML = []
        #self.wholeNewsLinks = []
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
                # newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
                # self.wholeNewsLinks.append(newsLinks)
                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                time.sleep(2)
        driver.quit()
        return self.wholeHTML

    def saveTo_localHtml(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_webpage.html" % (n, n1)
        with open(tmpFile, 'wt', encoding='utf-8') as htmlFile:
            htmlFile.write(str(self.wholeHTML))
        print(datetime.now())
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

        #
        #     exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
        #     splitNum = exmaxNum.split('/')
        #     maxNum = int(splitNum[1])
        #     print(maxNum)
        #     for pageId in range(maxNum):
        #         print(" pageId processing")
        #
        #         demo_div = driver.find_element_by_id('h.m.text')
        #         newsText = demo_div.get_attribute('innerHTML')
        #         self.wholeHTML.append(newsText.strip())
        #         driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
        #         time.sleep(2)
        # driver.quit()
        # return self.wholeHTML

    def scrape_news_line_bySoup(self):
        # Scrape title, source, showing time, news text between certain dates.
        # CSV file
        #html = driver.page_source
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_merged.csv" % (n, n1)
        csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showtime', 'showtime1', 'showtime2', 'newsText'])
        #driver = webdriver.PhantomJS()
        #self.textRow = []
        # self.textRow1 = []
        # self.textRow2 = []

        for html in self.wholeHTML:
            #self.textRow = []
            print("scrape_newsLine with Beautifulsoup self.wholeHTML processing")
            #print(html)
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

            #     find('span', class_='eh_edittime').text
            # # #newstitles = soup.findAll('a', attrs={'class':'nclicks'})
            # newstitles = soup.select('ul.mlist2 > li > a')
            # for newstitle in newstitles:
            #     self.textRow.append([newstitle.text.strip()])
            # sources = soup.findAll(attrs={'class': 'writing'})
            # for source in sources:
            #     self.textRow.append([source.text.strip()])
            # showtimes = soup.findAll(attrs={'class': 'eh_edittime'})
            # for showtime in showtimes:
            #     self.textRow.append([showtime.text.strip()])
            # writer.writerow(self.textRow)
            #
            # #
            # showtimelist = soup.select('ul.mlist2 > li > span.mlist2_info')
            #
            # for sh in showtimelist:
            #     sh2 = sh.findall('span', class_='eh_edittime')
            #     for sh3 in sh2:
            #         self.textRow2.append([sh3.text.strip()])
            #
            #     #showtime = sh.find('span', class_='eh_edittime').text
                #



            #print(newstitles)
            # self.textRow = [[newstitle.text.strip()] for newstitle in newstitles]
            # sources = soup.findAll(attrs={'class': 'writing'})
            # self.textRow1 = [[source.text.strip()] for source in sources]
            # self.textRow2 = []
            # showtimelist = soup.select('ul.mlist2 > li > span.mlist2_info')
            # for sh in showtimelist:
            #     showtime = sh.find('span', class_='eh_edittime').text
            #     #
                # showtime = sh.select('span.mlist2_info > span:nth-of-type(3)')[0].get_text()
                # showtime1 = sh.select('span.mlist2_info > span:nth-of-type(5)')[0].get_text()
                # showtime2 = sh.select('span.mlist2_info > span:nth-of-type(7)')[0].get_text()
                # #showtimemerged = showtime+showtime1+showtime2
                #self.textRow2.append(str(showtimemerged.get_text.strip())
                # self.textRow2.append(showtime)
            #
            # #for item in html:
            #     #print("scrape_newsText for item in html processing")
            # showtimes = soup.select('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(3)')
            # self.textRow2 = [[showtime.text.strip()] for showtime in showtimes]
            # print(self.textRow2)
            # # showtimes1 = soup.select('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(5)')
            # self.textRow3 = [[showtime.text.strip()] for showtime in showtimes1]
            # showtimes2 = soup.select('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(7)')
            # self.textRow4 = [[showtime.text.strip()] for showtime in showtimes2]
            #     # showtimes3 = soup.select('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(9)')
                # textRow5 = [[showtime.text.strip()] for showtime in showtimes3]
        #     for i in zip_longest(self.textRow, self.textRow1, self.textRow2, self.textRow3, self.textRow4, fillvalue='_'):
        #         writer.writerow(i)
        #
        # csvFile.close()
        #return
        #print(self.textRow, self.textRow1, self.textRow2)
        return self.textRow

    def scrape_news_line_bySelenium(self):
        self.linkFile = input("upload link file:")
        driver = webdriver.PhantomJS()
        driver.get(self.linkFile)
        #driver.get('file:///home/ham/Envs/scrapy/naverNews_2017_3_1_to_2017_3_2_webpage.html')
        #window_before = driver.window_handles[0]
        newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        self.textRow = [[newstitle.text.strip()] for newstitle in newsLinks]
        sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
        self.textRow1 = [[source.text.strip()] for source in sources]
        showtimelist = driver.find_elements_by_css_selector('ul.mlist2 > li > span.mlist2_info')
        self.textRow2 = []
        for sh in showtimelist:
            showtime = driver.find_elements_by_class_name('eh_edittime')
            for sh2 in showtime:
                self.textRow2.append(sh2.text.strip())
#
#
#             self.textRow2.append([sh.find('span', class_='eh_edittime').text.strip()])
# driver.find_element(By.CSS_SELECTOR, 'p.content:nth-child(1)')
#
#             showtime = driver.find_element_by_css_selector('span.mlist2_info > span:nth-of-type(3)')
#             showtime1 = driver.find_element_by_css_selector('span.mlist2_info > span:nth-of-type(5)')
#             showtime2 = driver.find_element_by_css_selector('span.mlist2_info > span:nth-of-type(7)')
#             showtimemerged = showtime+showtime1+showtime2
#             self.textRow2.append(showtimemerged.text.strip())
        return self.textRow, self.textRow1, self.textRow2

    def scrape_news_text_bySelenium(self):
        driver = webdriver.PhantomJS()
        driver.get(self.linkFile)
        window_before = driver.window_handles[0]
        newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        self.textRow5 = []
        for link in newsLinks:
            print("link Processing")
            link.click()
            #time.sleep(2)
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
            #time.sleep(5)
            newstextID = driver.find_element_by_id('articleBodyContents')
            newsText = newstextID.get_attribute('innerText')
            self.textRow5.append([newsText.replace('\n\n', '').strip()])
            #writer.writerow([newsText.replace('\n\n', '').strip()])
            driver.close()
            driver.switch_to_window(window_before)

        return self.textRow5
        #
        # showtimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(3)')
        # self.textRow2 = [[showtime.text.strip()] for showtime in showtimes]
        # showtimes1 = driver.find_elements_by_css_selector('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(5)')
        # self.textRow3 = [[showtime.text.strip()] for showtime in showtimes1]
        # showtimes2 = driver.find_elements_by_css_selector('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(7)')
        # self.textRow4 = [[showtime.text.strip()] for showtime in showtimes2]
        #newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        #print(newsLinks)



        #return self.textRow, self.textRow1, self.textRow2, self.textRow3, self.textRow4

    def scrape_WholeNews(self):
        print(datetime.now())
        # n = self.startDate.replace(',', '_')
        # n1 = self.endDate.replace(',', '_')
        # tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_newstext.csv" % (n, n1)
        # csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        # writer = csv.writer(csvFile)
        # writer.writerow(['newsTitle', 'source', 'showtime', 'newsText'])
        #writer.writerow(['newsTitle', 'source', 'showtime', 'showtime1', 'showtime2', 'newsText'])

        # #driver = webdriver.PhantomJS()
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
        # showtimes1 = driver.find_elements_by_css_selector('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(5)')
        # self.textRow3 = [[showtime.text.strip()] for showtime in showtimes1]
        # showtimes2 = driver.find_elements_by_css_selector('ul.mlist2 > li > span.mlist2_info > span:nth-of-type(7)')
        # self.textRow4 = [[showtime.text.strip()] for showtime in showtimes2]
        #newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        #print(newsLinks)

        print(datetime.now())
        self.textRow5 = []
        for link in newsLinks:
            print("link Processing")
            link.click()
            #time.sleep(2)
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
            #time.sleep(5)
            newstextID = driver.find_element_by_id('articleBodyContents')
            newsText = newstextID.get_attribute('innerText')
            self.textRow5.append([newsText.replace('\n\n', '').strip()])
            #writer.writerow([newsText.replace('\n\n', '').strip()])
            driver.close()
            driver.switch_to_window(window_before)
        #for i in zip_longest(self.textRow, self.textRow1, self.textRow2, self.textRow3, self.textRow4, self.textRow5, fillvalue='_', encoding='utf-8'):

        # for i in zip_longest(self.textRow, self.textRow1, self.textRow2, self.textRow5, fillvalue='_', encoding='utf-8'):
        #     writer.writerow(i)
        #d = datetime.now()
        print(datetime.now())
        #
        # n = self.startDate.replace(',', '_')
        # n1 = self.endDate.replace(',', '_')
        # tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_webpage.csv" % (n, n1)
        # with open(tmpFile, 'wt', encoding='utf-8') as htmlFile:
        #     for tr in textRow5:
        #         htmlFile.write(str(tr))
        driver.quit()
        print(self.textRow5)
        return

    def merge_lists_saveCsv(self):
        print(datetime.now())
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_newstext.csv" % (n, n1)
        csvFile = open(tmpFile, 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(['newsTitle', 'source', 'showtime', 'newsText'])
        #for i in zip_longest(self.textRow, self.textRow1, self.textRow2, self.textRow5, fillvalue='_'):
        for i in zip_longest(self.textRow, self.textRow1, self.textRow2, fillvalue='_'):
            writer.writerow(i)
        return

        #
        #
        # self.textRow5 = []
        #
        # for url in self.urls:
        #     print("scrape_bodyText url processing")
        #     driver = webdriver.PhantomJS()
        #     driver.get(url)
        #     window_before = driver.window_handles[0]
        #     exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
        #     splitNum = exmaxNum.split('/')
        #     maxNum = int(splitNum[1])
        #     print(maxNum)
        #     #self.textRow5 = []
        #     i = 0
        #     #newsLists = []
        #     for pageId in range(maxNum):
        #         print("scrape_bodyText pageId processing")
        #         #window_before = driver.window_handles[0]
        #         newsLinks = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
        #         for i in range(len(newsLinks)):
        #             print("scrape_bodyText i processing")
        #             #window_before = driver.window_handles[0]
        #             #window_before = driver.window_handles[0]
        #             # newsLists.append(newsLinks)
        #             #driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
        #             #time.sleep(2)
        #             # for newstitle in newsLinks:
        #             #print("scrape_bodyText newstitle processing")
        #                 #window_before = driver.window_handles[0]
        #             #
        #             newsLinks[i].click()
        #             time.sleep(2)
        #             window_after = driver.window_handles[1]
        #             driver.switch_to_window(window_after)
        #             wait = WebDriverWait(driver, 20)
        #             wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))
        #             #time.sleep(5)
        #             newstextID = driver.find_element_by_id('articleBodyContents')
        #             newsText = newstextID.get_attribute('innerText')
        #             self.textRow5.append([newsText.replace('\n\n', '').strip()])
        #             #writer.writerow([newsText.replace('\n\n', '').strip()])
        #
        #             driver.close()
        #             driver.switch_to_window(window_before)
        #             driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
        #
        #             time.sleep(2)
        #             i = i+1
        # print(self.textRow5)
        # # for i in zip_longest(self.textRow, self.textRow1, self.textRow2, self.textRow3, self.textRow4, self.textRow5, fillvalue='_'):
        # #     writer.writerow(i)
        # driver.quit()
        # return self.textRow5

    def saveToCsvFile(self):
        n = self.startDate.replace(',', '_')
        n1 = self.endDate.replace(',', '_')
        tmpFile = "/home/ham/Envs/scrapy/naverNews_%s_to_%s_newstext.csv" % (n, n1)
        with open(tmpFile, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            for i in self.textRow5:
                writer.writerow(i)
        csvFile.close()
        return

            #writer.writerow(['newsTitle', 'source', 'showtime', 'showtime1', 'showtime2', 'newsText'])
        #driver = webdriver.PhantomJS()
        # for i in zip_longest(self.textRow, self.textRow1, self.textRow2, self.textRow3, self.textRow4, self.textRow5, fillvalue='_'):
        #     writer.writerow(i)

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
        a.get_wholeHtml()
        a.saveTo_localHtml()
        a.scrape_news_line_bySoup()
        #a.scrape_news_line_bySelenium()
        #a.scrape_news_text_bySelenium()
        #a.scrape_WholeNews()
        #a.merge_lists_saveCsv()

        #a.scrape_WholeNews()
        #a.scrape_newsline()
        #a.get_wholeHtml()

        # print ('scraping and save to Csv file...')
        #a.scrape_saveCsv()
        # print ('converting csv file to dictionary')
        #a.scrape_newsText()
        #a.scrape_bodyText()
        # a.saveToCsvFile()
        # # print ('scraping news Text...')
        #a.duplicateItemRemove()
        #a.merge_twoCsvs()
        # # a.csvToDic()
        # print ('sending dictionay to Mysql..')
        # a.dicToMysql()
