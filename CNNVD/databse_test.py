#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Time    : 19-5-27 下午2:13
# @Author  : tang
# @File    : databse_test.py

import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['test']
collection = db['students']
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

print (type(student))
result = collection.insert(student)
print(result)