#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Time    : 19-5-28 下午2:36
# @Author  : tang
# @File    : interpret.py

from bs4 import BeautifulSoup
from lxml.html import fromstring
from CNNVD.Other_info import get_other_info
from CNNVD.insert_to_mongodb import insert_to_databse
def interpret_html(Html):
    CNNVD = {}
    print('Parsing!')
    # print(Html)
    parser = fromstring(Html)
    information = parser.xpath('/html/body/div[4]/div/div[1]/div[1]/h2/text()')[0]
    detail = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/h2/text()')[0]
    CNNNVD_number = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[1]/span/text()')[0]
    CNNNVD_number = CNNNVD_number.split('：')[-1]
    severity = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[2]/a/text()')[0]
    severity = severity.replace('\t','').replace('\r','').replace('\n','')
    cve_number = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[3]/a/text()')[0]
    cve_number = cve_number.replace('\t','').replace('\r','').replace('\n','').replace(' ','')
    vulnersbility_type = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[4]/a/text()')[0]
    vulnersbility_type = vulnersbility_type.replace('\t','').replace('\r','').replace('\n','').replace(' ','')
    publish_date = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[5]/a/text()')[0]
    publish_date = publish_date.replace('\t','').replace('\r','').replace('\n','').replace(' ','')
    threat_type = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[6]/a/text()')[0]
    update_date = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[7]/a/text()')[0]
    factory = parser.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[8]/text()')[0]
    threat_type = threat_type.replace('\t','').replace('\r','').replace('\n','')
    update_date = update_date.replace('\t','').replace('\r','').replace('\n','')
    factory = factory.replace('\t','').replace('\r','').replace('\n','').replace(' ', '')
    source = parser.xpath('//*[@id="1"]/text()')[0]
    source = source.replace('\t','').replace('\r','').replace('\n','')
    # print(information, detail, CNNNVD_number, severity, cve_number, vulnersbility_type, publish_date, threat_type, update_date, factory, source)
    CNNVD['CNNVD编号'] = CNNNVD_number
    CNNVD['漏洞信息详情'] = {'title': detail, '危害等级' : severity, 'CVE编号' : cve_number, \
                       '漏洞类型' : vulnersbility_type, '发布时间' : publish_date, '威胁类型' : threat_type, \
                       '更新时间' : update_date, '厂商' : factory, '漏洞来源' : source}
    ldjj, ldgg, ckwz, syxst, bd = get_other_info(Html)
    CNNVD['漏洞简介'] = ldjj
    CNNVD['漏洞公告'] = ldgg
    CNNVD['参考网址'] = ckwz
    CNNVD['受影响实体'] = syxst
    CNNVD['补丁'] = bd
    print(CNNVD)
    insert_msg = insert_to_databse(CNNVD)
    # if insert_msg is not None:
    #     print("Insert a record into database.")
    return CNNVD


