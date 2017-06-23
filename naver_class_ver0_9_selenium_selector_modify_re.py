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
from selenium.common.exceptions import WebDriverException
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

    # driver.get("javascript:document.getElementById('overridelink').click();");
    # String winHandleBefore = driver.getWindowHandle();
    # main_window = driver.current_window_handle
    # elemento = WebDriverWait(driver, 15).until(lambda driver:driver.find_element_by_id('MainContent_Buscador2_cboUbicacion1'))
    # url = urlSchool.get_attribute('href')
    # driver.get(url)

        for url in self.urls:
            print("url processing")
            driver.get(url)
            main_window = driver.current_window_handle
            #window_before = driver.window_handles[0]
            # Get max page number of current url
            exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
            splitNum = exmaxNum.split('/')
            maxNum = int(splitNum[1])
            print(maxNum)
            # Get titles, news texts etc of the current page
            for pageId in range(maxNum):
                print(" pageId processing")
                #driver.implicitly_wait(60)
                # %%%%%%%% driver.find_elements_by_xpath("//div[contains(@class, 'foo')]")
                #newstitles = driver.find_elements_by_xpath("//a[contains(@class, 'nclicks')]")
                #driver.implicitly_wait(200)
                #driver.implicitly_wait(200)
                time.sleep(5)
                # '//span[contains(@class,"eh_edittime")]'
                #newstitles = driver.find_elements_by_xpath('//a[contains(@target,"_blank")]')

                newstitles = driver.find_elements_by_css_selector('ul.mlist2 > li > a')
                #driver.implicitly_wait(10)
                textRow = [[newstitle.text.strip()] for newstitle in newstitles]
                sources = driver.find_elements_by_xpath('//span[contains(@class,"writing")]')
                #sources = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing')
                #driver.implicitly_wait(10)
                textRow1 = [[source.text.strip()] for source in sources]
                showtimes = driver.find_elements_by_xpath('//span[contains(@class,"eh_edittime")]')
                #showtimes = driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.eh_edittime')
                #driver.implicitly_wait(10)
                textRow2 = [[showtime.text.strip()] for showtime in showtimes]
                driver.implicitly_wait(200)
                #driver.implicitly_wait(200)

                textRow3 = []
                for newstitle in newstitles:
                    print("inner text processing")
                    #old_page = driver.find_element_by_class_name('mlist2')
                    driver.implicitly_wait(100)
                    newstitle.click()
                    # wait = WebDriverWait(driver, 100)
                    # wait.until(EC.visibility_of_element_located((By.ID, 'chrome')))
                    #driver.implicitly_wait(200)
                    time.sleep(5)
                    #driver.implicitly_wait(20)\time.
                    # driver.implicitly_wait(20)
                    # wait = WebDriverWait(driver, 60)
                    # #wait.until(EC.invisibility_of_element_located((By.TAG_NAME, 'ul')))
                    # # wait = WebDriverWait(driver, 60)
                    # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'mlist2')))
                    #old_page = driver.find_element_by_class_name('mlist2')
                    # wait = WebDriverWait(driver, 60)
                    #wait.until(EC.staleness_of(old_page))

                    # window_before = driver.window_handles[0]
                    # driver.switch_to_window(window_before)

                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)


                    #driver.implicitly_wait(100)
                    wait = WebDriverWait(driver, 100)
                    # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="articleBodyContents"]')))
                    wait.until(EC.visibility_of_element_located((By.ID, 'articleBodyContents')))

                    demo_div = driver.find_element_by_id('articleBodyContents')
                    newsText = demo_div.get_attribute('innerText')
                    #driver.implicitly_wait(200)
                    textRow3.append([newsText.replace('\n\n', '').strip()])
                    driver.close()
                    #driver.back()

                    #driver.switch_to_window(window_before)
                    driver.switch_to_window(main_window)
                    #driver.implicitly_wait(20)

                # Merge produced list files
                for i in zip_longest(textRow, textRow1, textRow2, textRow3, fillvalue='_'):
                    writer.writerow(i)


                # wait = WebDriverWait(driver, 20)
                # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="h.m.text"]/div/div[2]/a[2]')))
                #driver.switch_to_window(window_before)
                # old_page = driver.find_element_by_tag_name('html')
                # #old_page = driver.find_element_by_nameclass_name('mlist2')
                # wait = WebDriverWait(driver, 20)
                # wait.until(EC.staleness_of(old_page))

                # wait = WebDriverWait(driver, 20)
                # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'mlist2')))
                #driver.switch_to_window(window_before)

                #driver.close()
                #driver.switch_to_window(window_before)
                wait = WebDriverWait(driver, 100)
                # wait.until(EC.visibility_of_element_located((By.ID, 'h.m.text')))
                wait.until(EC.visibility_of_element_located((By.ID, 'wrap')))

                driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
                window_before = driver.window_handles[0]
                driver.switch_to_window(window_before)
                # window_after = driver.window_handles[1]
                # driver.switch_to_window(window_after)
                # u = driver.current_url
                # driver.get(u)
                # wait = WebDriverWait(driver, 100)
                # # wait.until(EC.visibility_of_element_located((By.ID, 'h.m.text')))
                # wait.until(EC.visibility_of_element_located((By.ID, 'wrap')))
                # wait = WebDriverWait(driver, 100)
                # wait.until(EC.visibility_of_element_located((By.ID, 'h.m.text')))
                # She sees that her list is in there, named according to its


                # first list item
    #             self.browser.find_element_by_link_text('Reticulate splines').click()
    #             self.assertEqual(self.browser.current_url, first_list_url)
    #             # She sees that her list is in there, named according to its
    #             # first list item
    #             self.browser.find_element_by_link_text('Reticulate splines').click()
    #             self.wait_for(
    #                 lambda: self.assertEqual(self.browser.current_url, first_list_url)
    #             )
    #             from selenium.common.exceptions import WebDriverException
    #
    #
    # def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
    #     start_time = time.time()
    #     while time.time() - start_time < timeout:
    #         try:
    #             return function_with_assertion()
    #         except (AssertionError, WebDriverException):
    #             time.sleep(0.1)
    #     # one more try, which will raise any errors if they are outstanding
    #     return function_with_assertion()
    #


                #time.sleep(5)
                #driver.getCurrentUrl()


                #driver.implicitly_wait(30)
                #time.sleep(2)
                #driver.switch_to_window(window_before)
                # window_after = driver.window_handles[1]
                # driver.switch_to_window(window_after)

                #time.sleep(5)
                #driver.implicitly_wait(30)
                #driver.current_url
                #driver.page_source
                #driver.switch_to_window(window_before)
                # wait = WebDriverWait(driver, 30)
                # # #wait.until(EC.visibility_of_all_elements_located((By.ID, 'h.m.text')))
                # # # # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'mlist2')))
                # # # #
                # # # #WebDriverWait(browser, delay).until(EC.presence_of_element_located(By.ID, 'IdOfMyElement'))
                # wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.mlist2 > li > a')))
                # wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.mlist2 > li > span > span.writing')))
                # wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.mlist2 > li > span > span.eh_edittime')))
                #newstitles = driver.find_elements_by_xpath("//span[contains(@class, 'writing')]")
                # wait.until(EC.visibility_of((By.XPATH, '//span[contains(@class, "writing")]')))
                # wait.until(EC.visibility_of((By.XPATH, '//span[contains(@class, "eh_edittime")]')))
                # wait.until(EC.visibility_of((By.CSS_SELECTOR, 'ul.mlist2 > li > a')))
                #
                # wait.until(EC.visibility_of((By.CSS_SELECTOR, 'ul.mlist2 > li > span > span.writing')))
                # wait.until(EC.visibility_of((By.CSS_SELECTOR, 'ul.mlist2 > li > span > span.eh_edittime')))
                # wait.until(EC.visibility_of((By.CSS_SELECTOR, 'ul.mlist2 > li > a')))

                # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'mlist2')))
                # # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'writing')))
                # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'eh_edittime')))
                # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mlist2 > li > span > span.writing')))
                # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mlist2 > li > span > span.eh_edittime')))
                # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.mlist2 > li > a')))
                # wait.until(EC.element_to_be_selected((driver.find_elements_by_css_selector('ul.mlist2 > li > a'))))
                # wait.until(EC.element_to_be_selected((driver.find_elements_by_css_selector('ul.mlist2 > li > span > span.writing'))))
                # wait.until(EC.element_to_be_selected((driver.find_elements_by_css_selector('ul.mlist2 > li > a'))))
                #time.sleep(5)

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
