# -*- coding: UTF-8 -*-

from selenium import webdriver
import time



def get_info(url):
    browser.get(url)
    CNNVD_id = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[1]/span').text
    title = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/h2').text
    serverity = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[2]').text
    cve_number = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[3]').text
    vulnersbility_type = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[4]').text
    publish_date = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[5]').text
    threat_type = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[6]').text
    update_date = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[7]').text
    factory = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[8]').text
    source = browser.find_element_by_xpath('//*[@id="1"]').text
    intr = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[3]').text
    notice = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[4]').text
    ref = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[5]').text
    affected = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[6]').text
    patch = browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[7]/div[3]/ul/li/div[1]/a').text


if __name__ == '__main__':
    browser = webdriver.Firefox()
    # url = 'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201905-00'
    # for i in range(1,100):
    #     URL = url + str(i)
    #     get_info(URL)
    #     time.sleep(5)
    time.sleep(2)
    browser.get("http://httpbin.org/ip")
    print(browser.page_source)
    browser.close()


