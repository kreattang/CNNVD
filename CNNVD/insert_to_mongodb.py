#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Time    : 19-5-29 下午4:11
# @Author  : tang
# @File    : insert_to_mongodb.py

import pymongo
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['CNNVD']
mycol = mydb["CNNVD_data"]

def insert_to_databse(CNNVD):
    CNNVD_number = CNNVD['CNNVD编号']
    print(CNNVD_number)
    if mycol.find_one({'CNNVD编号' : CNNVD_number}) is None:
        mycol.insert_one(CNNVD)
        print("Insert a record into database.")
    else:
        print('Data duplication')
