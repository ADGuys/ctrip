# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import pymongo
import json
import time
import random

import scrapy
from scrapy import signals
from twisted.internet.error import TimeoutError, ConnectionRefusedError

pool = []


class HttpbinProxyMiddleware(object):

    def process_request(self, request, spider):
        myclient = pymongo.MongoClient("mongodb://40.73.115.215:27017/")
        mydb = myclient["proxy_pool"]
        mydb.authenticate("proxy", "Loctek#2020")
        mycol = mydb["proxy_xdaili"]

        if not pool:
            print('pool 空了')
            data = mycol.find({}, {'_id': 0, 'name': 1, 'state': 1})
            for i in data:
                if i['state'] == 1:
                    pool.append(i['name'])

        else:
            ip = pool[-1]
            print("ip: ", ip)
            request.meta['proxy'] = 'https://{}'.format(str(ip))

    def process_response(self, response, request, spider):
        response_json = json.loads(response.text)
        if response_json['rlt'] == 508:  # ip过期
            pool.pop()
            if not pool:
                time.sleep(300)
            return request
        else:
            return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            pool.pop()
            print('timeout error')
            print('have pool:', pool)
            # pool.pop()
        if isinstance(exception, ConnectionRefusedError):
            pool.pop()
            print('connect error')
            print('pool pop in process exception')
            # if isinstance(exception, )
        if not pool:
            time.sleep(300)
