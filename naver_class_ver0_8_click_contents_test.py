"""coded by Ham."""

import csv
from selenium import webdriver
import time
driver = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')
#driver = webdriver.PhantomJS()
url = 'http://news.naver.com/main/history/mainnews/list.nhn'
driver.get(url)
window_before = driver.window_handles[0]
#try:
exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
splitNum = exmaxNum.split('/')
maxNum = int(splitNum[1])
print(maxNum)
#newsTextRow = []
#tmpFile = "/home/ham/Envs/scrapy/test_newstext.csv"
csvFile = open("/home/ham/Envs/scrapy/test_newstext.csv", 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
#writer = csv.DictWriter(csvFile, fieldnames=["textNews"])
#writer.writeheader()
writer.writerow(['textNews'])
#itemTuples = []

#try:
for pageId in range(maxNum):
    itemTuples = []
    #dataRow = []
    for i in range(1, 5):
        for j in range(1, 6):
            itemTuples.append((i, j))
    print(itemTuples)
    for i in itemTuples:
        dataRow = []
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
        dataRow.append([newsText.replace('\n\n', '').strip()])
        driver.close()
        driver.switch_to_window(window_before)
        time.sleep(2)
        print(dataRow)
        writer.writerow(dataRow)
    #writer.write(dataRow)
    driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
    time.sleep(5)
    # driver.page_source
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # scrap = soup.select('ul.mlist2 > li')
    # #print(newsTextRow[0])
# else:
#print(dataRow)
driver.quit()
csvFile.close()
#except Exception as e:
#    print(e)
