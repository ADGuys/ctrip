# -*- coding: utf-8 -*-
import scrapy
import json
import hashlib
from scrapy.http import Request, FormRequest
from .base import ListDetailExtractData, OZ
# from ..utlis.utlis import HttpProxy, req
from datetime import date, timedelta
from xpinyin import Pinyin
from ..items import CtripItem
import requests


class OperationSpider(scrapy.Spider):
    name = 'operation'
    allowed_domains = ['m.ctrip.com']
    start_urls = ['https://m.ctrip.com/']

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS': 1,
    }

    url = 'https://m.ctrip.com/restapi/soa2/14022/flightListSearch?_fxpcqlniredt=09031172313706160008'

    def start_requests(self):
        list_city = ListDetailExtractData.read_excel_to_dict()
        # meta_proxy = 'http://125.116.16.91:43751/'
        for y in range(0, len(list_city)):
            for j in range(0, len(list_city)):
                qidian = list_city[y]['ThreeCode']
                luodian = list_city[j]['ThreeCode']
                yesterday0 = date.today() + timedelta(days=+2)
                yesterday1 = date.today() + timedelta(days=+1)
                yesterday2 = date.today() + timedelta(days=+0)
                # yesterday3 = date.today() + timedelta(days=+3)
                yesterday = [yesterday1, yesterday2]
                for x in range(0, len(yesterday)):
                    formdata = {
                        "contentType": "json",
                        "flag": 8,
                        "trptpe": '1',
                        "searchitem": [{
                            "dccode": qidian,  # 起始
                            "accode": luodian,  # 到达
                            "dtime": yesterday[x].strftime('%Y-%m-%d')  # (\d+-\d+-\d+) 2020-01-01
                        }],
                        "head": {
                            "auth": "null",
                            "ctok": "",
                            "cver": "1.0",
                            "lang": "01",
                            "sid": "8888",
                            "syscode": "09",
                            "preprdid": ""
                        },
                    }
                    if formdata["searchitem"][0]['dccode'] != formdata["searchitem"][0]['accode']:
                        yield Request(self.url, body=json.dumps(formdata), method='POST')

    def parse(self, response):
        data = json.loads(response.text)['fltitem']
        # print(data)
        for i in data:
            # 航班号
            flight = i['mutilstn'][0]['basinfo']['flgno']
            # print(flight)
            # 出发城市
            departCity = i['mutilstn'][0]['dportinfo']['cityname']
            # 出发城市拼音
            p = Pinyin()
            dCityPinYin = p.get_pinyin(departCity, '')
            # 出发机场代码
            dPortCode = i['mutilstn'][0]['dportinfo']['city']
            # 出发机场
            dPort = i['mutilstn'][0]['dportinfo']['aportsname'] + i['mutilstn'][0]['dportinfo']['bsname']
            # 到达城市
            arriveCity = i['mutilstn'][0]['aportinfo']['cityname']
            # 到达城市拼音
            aCityPinYin = p.get_pinyin(arriveCity, '')
            # 到达机场
            aPort = i['mutilstn'][0]['aportinfo']['aportsname'] + i['mutilstn'][0]['aportinfo']['bsname']
            # 到达机场代码
            aPortCode = i['mutilstn'][0]['aportinfo']['city']

            ddate = i['mutilstn'][0]['dateinfo']['ddate']
            # 起飞时间
            takeOffTime = ddate[11:16]
            # 出发日期
            startDate = ddate[:4] + ddate[4:7] + ddate[7:10]

            adate = i['mutilstn'][0]['dateinfo']['adate']
            # 到达时间
            arriveTime = adate[11:16]
            # 到达日期
            endDate = adate[:4] + adate[4:7] + adate[7:10]
            # 票价
            standardPrice = i['policyinfo'][0]['priceinfo'][0]['price']
            # 票数
            quantity = i['policyinfo'][0]['priceinfo'][0]['ticket']
            # 票价
            price = i['policyinfo'][0]['priceinfo'][0]['price']
            # 航空公司
            try:
                airline = i['mutilstn'][0]['basinfo']['aircode']
                airlines = OZ[airline]
            except:
                airlines = '国际航空'
            # 飞机信息
            aplaneModel = i['mutilstn'][0]['craftinfo']['cname'] + \
                          i['mutilstn'][0]['craftinfo']['craft'] + \
                          '(' + i['mutilstn'][0]['craftinfo']['kind'] + ')'
            # print(flight,departCity,dCityPinYin,dPortCode,dPort,arriveCity,aCityPinYin,aPort,aPortCode,takeOffTime,startDate,arriveTime,endDate,standardPrice,quantity,price,airline,aplaneModel)
            itme = CtripItem()
            itme['flight'] = flight
            itme['departCity'] = departCity
            itme['dCityPinYin'] = dCityPinYin
            itme['dPortCode'] = dPortCode
            itme['dPort'] = dPort
            itme['arriveCity'] = arriveCity
            itme['aCityPinYin'] = aCityPinYin
            itme['aPort'] = aPort
            itme['aPortCode'] = aPortCode
            itme['takeOffTime'] = takeOffTime
            itme['startDate'] = startDate
            itme['arriveTime'] = arriveTime
            itme['endDate'] = endDate
            itme['airline'] = airlines
            itme['aplaneModel'] = aplaneModel
            itme['quantity'] = quantity
            jiami = hashlib.md5(str(itme).encode(encoding='UTF-8')).hexdigest()
            itme['standardPrice'] = standardPrice
            itme['price'] = price
            itme['md5'] = jiami
            yield itme
