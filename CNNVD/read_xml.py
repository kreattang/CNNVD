#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Time    : 19-6-7 下午1:36
# @Author  : tang
# @File    : read_xml.py

# -*- coding: UTF-8 -*-
import json
import xmltodict
import os
from CNNVD.insert_to_mongodb import insert_to_databse

def Get_all_name(filePath):
    file_names = []
    for i in os.listdir(filePath):
        file_names.append(i)
    return file_names

def xml2json(file_name):
    with open(file_name, 'r', encoding='UTF-8') as f:
        xmlString = f.read()
    jsonString = json.dumps(xmltodict.parse(xmlString), ensure_ascii=False, indent=4)
    output = json.loads(jsonString)
    # print(len(output['cnnvd']['entry']))
    entry = output['cnnvd']['entry']
    for e in entry:
        CNNVD = {}
        CNNVD['CNNVD编号'] = e['vuln-id']
        CNNVD['漏洞信息详情'] = {'title': e['name'], '危害等级': e['severity'], 'CVE编号': e['other-id']['cve-id'], \
                           '漏洞类型': e['vuln-type'], '发布时间': e['published'], '威胁类型': e['thrtype'], \
                           '更新时间': e['modified'], '漏洞来源': e['source']}
        CNNVD['漏洞简介'] = e['vuln-descript']
        CNNVD['漏洞公告'] = e['vuln-solution']
        refs = []
        if e['refs'] is not None:
            ref = e['refs']['ref']
            if type(ref) is dict:
                temp = {}
                temp['来源'] = str(ref['ref-source'])
                temp['名称'] = str(ref['ref-name'])
                temp['链接'] = str(ref['ref-url'])
                refs.append(temp)
            else:
                for r in e['refs']['ref']:
                    temp = {}
                    temp['来源'] = str(r['ref-source'])
                    temp['名称'] = str(r['ref-name'])
                    temp['链接'] = str(r['ref-url'])
                    refs.append(temp)
        CNNVD['参考网站'] = refs
        syxst = []
        vuln_list = e['vuln-software-list']
        if vuln_list is not None:
            software_list = vuln_list['product']
            syxst = software_list
        CNNVD['受影响实体'] = syxst
        # print(CNNVD)
        insert_to_databse(CNNVD)
    print('finish!')



if __name__ == '__main__':
    file_names = Get_all_name('/home/wenbing/Desktop/CNNVD_dataset')
    for f in file_names:
        print(f)
        xml2json('/home/wenbing/Desktop/CNNVD_dataset/'+str(f))

# xml2json('/home/wenbing/Desktop/CNNVD_dataset/2015.xml')
# 2004meiyou