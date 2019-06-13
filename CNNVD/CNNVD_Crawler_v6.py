#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Time    : 19-6-3 上午10:56
# @Author  : tang
# @File    : CNNVD_Crawler_v6.py


from requests.exceptions import ConnectionError
from lxml.html import fromstring
from itertools import cycle
import concurrent.futures
import random
import requests
import time
from timeloop import Timeloop
from datetime import timedelta
import datetime
from CNNVD.interpret import interpret_html


PROXIES = []
PROXY_POOL = None
NUM_WORKERS = 4
REFRESH_TIMEOUT = 300  # In seconds

USER_AGENTS = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
]


def refresh_proxies():
    def get_new_proxies_list():
        url = 'https://free-proxy-list.net/'
        user_agent = random.choice(USER_AGENTS)
        headers1 = {'User-Agent': user_agent}
        proxies1 = {'http': '221.216.136.215:9000'}
        response = requests.get(url, headers = headers1)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:20]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ':'.join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return list(proxies)

    # Get new proxies
    proxies = get_new_proxies_list()
    counter = 10
    # Retry after 1 second, for a maximum of 10 times
    while not len(proxies) and counter:
        counter -= 1
        time.sleep(1)
        proxies = get_new_proxies_list()

    # Update global variables if successfully obtained new list
    if len(proxies):
        global PROXIES, PROXY_POOL
        PROXIES = proxies
        PROXY_POOL = cycle(PROXIES)

def get_all_ip(file_name):
    ip = []
    with open(file_name, 'r') as f:
        data = f.readlines()  # txt中所有字符串读入data
        for line in data:
            ip.append(line[:-1])
    return ip

if __name__ == '__main__':
    refresh_proxies()
    PROXIES = get_all_ip('/home/wenbing/Desktop/UAV_Collision_Sim/CNNVD/Free-Proxy-IP-Crawler/proxy.txt')
    PROXY_POOL = cycle(PROXIES)
    URL = 'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-200412-'
    print("Current ip pool:",PROXIES)
    page = 1000
    times = 0
    while page > 0:
        times = times + 1
        url = ''
        if page >= 100:
            url = URL + str(page)
        if page < 100 and page >= 10:
            url = URL + '0' + str(page)
        if page < 10 and page > 0:
            url = URL + '00' + str(page)
        print('URL:', url)
        try:
            proxy = next(PROXY_POOL)
            print(f'Crawling {url.split("=")[-1]} using {proxy}.')
            user_agent = random.choice(USER_AGENTS)
            headers = {'User-Agent': user_agent}
            response = requests.get(url,
                                    headers=headers,
                                    proxies={'http': proxy, 'https': proxy}, timeout=30)
            if response.status_code == 200:
                html = response.text
                interpret_html(html)
                last_page= page
                page = page - 1
                times = 0
            if times >= 10:
                last_page = page
                page = page - 1
                times = 0


        except :
            # Bad IP address, retry
            print(f'Error, retrying.')
            if times >= 10:
                last_page = page
                page = page - 1
                times = 0
