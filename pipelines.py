# # -*- coding: utf-8 -*-

# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from datetime import date, timedelta
import time, requests

import socket


class CtripPipeline(object):
    # pass
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='loctek-echo-office.mysql.database.chinacloudapi.cn',  # 数据库地址
            port=3306,  # 数据库端口
            db='echo_office',  # 数据库名
            user='loctek-user@loctek-echo-office',  # 数据库用户名
            passwd='Cr8ef4aiW6BFUU',  # 数据库密码
            # charset='utf8',  # 编码方式
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.connect.ping(reconnect=True)
        # print(self.connect)
        self.cursor = self.connect.cursor()
        # self.cursor.ping(reconnect=True)
        sqls = '''select * from echo_flights_spare where md5 = %s'''
        # print(sqls)
        va = (str(item['md5']))
        self.cursor.execute(sqls, va)
        # Receive all return results
        results1 = self.cursor.fetchall()
        # self.cursor.execute(sqls)
        results = len(results1)
        if results == 0:
            self.cursor.execute(
                """insert into echo_flights_spare( md5,flight, departCity, dCityPinYin, dPort, dPortCode, arriveCity, aCityPinYin, aPort, aPortCode, takeOffTime,startDate, arriveTime, endDate, airline, aplaneModel, standardPrice, quantity, price) value ("{}", "{}","{}","{}","{}","{}","{}","{}","{}","{}","{}", "{}","{}","{}","{}","{}","{}","{}","{}")""".format(
                    str(item["md5"]), str(item["flight"]), str(item["departCity"]), str(item["dCityPinYin"]),
                    str(item["dPort"]), str(item["dPortCode"]), str(item["arriveCity"]), str(item["aCityPinYin"]),
                    str(item["aPort"]), str(item["aPortCode"]), str(item["takeOffTime"]), str(item["startDate"]),
                    str(item["arriveTime"]), str(item["endDate"]), str(item["airline"]), str(item["aplaneModel"]),
                    str(item["standardPrice"]), str(item["quantity"]), str(item["price"])))
            # 执行sql
            self.connect.commit()
        else:
            sql = ''' UPDATE echo_flights_spare SET price= %s WHERE md5= %s'''
            val = (str(item['price']), str(item['md5']))
            self.cursor.execute(sql, val)  # item里面定义的字段和表字段对应
            # 提交sql语句
            self.connect.commit()
            # print('更新数据')
        # return item
