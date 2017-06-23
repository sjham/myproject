"""coded by Ham."""

import csv
from selenium import webdriver
import time

driver = webdriver.Chrome('/media/sf_share_u/chromedriver_linux64/chromedriver')
#driver = webdriver.PhantomJS()
url = 'http://news.naver.com/main/history/mainnews/list.nhn'
driver.get(url)
window_before = driver.window_handles[0]
exmaxNum = driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[1]').text
splitNum = exmaxNum.split('/')
maxNum = int(splitNum[1])
print(maxNum)
csvFile = open("/home/ham/Envs/scrapy/test_newstext.csv", 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
#writer = csv.DictWriter(csvFile, fieldnames=["textNews"])
#writer.writeheader()
writer.writerow(['newsText'])
itemTuples = []
for i in range(1, 5):
    for j in range(1, 6):
        itemTuples.append((i, j))
for pageId in range(maxNum):
    for i in itemTuples:
        textRow = []
        driver.find_element_by_xpath('//*[@id="h.m.text"]/ul[%d]/li[%d]/a' % i).click()
        window_after = driver.window_handles[1]
        driver.switch_to_window(window_after)
        time.sleep(2)
        demo_div = driver.find_element_by_id("articleBodyContents")
        newsText = demo_div.get_attribute('innerText')
        textRow.append([newsText.replace('\n\n', '').strip()])
        driver.close()
        driver.switch_to_window(window_before)
        time.sleep(2)
        print(textRow)
        writer.writerow(textRow)
    driver.find_element_by_xpath('//*[@id="h.m.text"]/div/div[2]/a[2]').click()
    time.sleep(5)
driver.quit()
csvFile.close()
