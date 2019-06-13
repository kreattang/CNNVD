#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Time    : 19-5-29 下午3:45
# @Author  : tang
# @File    : Other_info.py

from bs4 import BeautifulSoup

def get_other_info(Html):
    soup = BeautifulSoup(Html, "lxml")
    lddata = soup.find_all('div', class_='d_ldjj')
    ldjj, ldgg, ckwz, syxst, bd = [], [], [], [], []
    for l in lddata:
        if l.h2.string == '漏洞简介':
            ldjj = l
        if l.h2.string == '漏洞公告':
            ldgg = l
        if l.h2.string == '参考网址':
            ckwz = l
        if l.h2.string == '受影响实体':
            syxst = l
        if l.h2.string == '补丁':
            bd = l
    ldjj_temp = ''
    for i in ldjj.find_all('p'):
        ldjj_temp = ldjj_temp + i.string.replace(' ', '').replace('\t','').replace('\r','').replace('\n','')
    # print(ldjj_temp)
    ldgg_temp = ''
    for _ in ldgg.find_all('p'):
        ldgg_temp = ldgg_temp + _.string.replace(' ', '').replace('\t','').replace('\r','').replace('\n','')
    # print(ldgg_temp)
    ckwz_temp = ''
    for __ in ckwz.find_all('p'):
        ckwz_temp = ckwz_temp + __.string.replace(' ', '').replace('\t','').replace('\r','').replace('\n','')
    # print(ckwz_temp)
    syxst_temp = ''
    for j in syxst.find_all('p'):
        syxst_temp = syxst_temp + j.string.replace(' ', '').replace('\t','').replace('\r','').replace('\n','')
    # print(syxst_temp)
    bd_temp = ''
    for k in bd.find_all('a', class_='a_title2'):
        bd_temp = bd_temp + k.string.replace('\t','').replace('\r','').replace('\n','')
    return ldjj_temp, ldgg_temp, ckwz_temp, syxst_temp, bd_temp

