# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CtripItem(scrapy.Item):
    flight = scrapy.Field()
    departCity = scrapy.Field()
    dCityPinYin = scrapy.Field()
    dPortCode = scrapy.Field()
    dPort = scrapy.Field()
    arriveCity = scrapy.Field()
    aCityPinYin = scrapy.Field()
    aPort = scrapy.Field()
    aPortCode = scrapy.Field()
    takeOffTime = scrapy.Field()
    startDate = scrapy.Field()
    arriveTime = scrapy.Field()
    endDate = scrapy.Field()
    airline = scrapy.Field()
    aplaneModel = scrapy.Field()
    standardPrice = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    md5 = scrapy.Field()
    ip = scrapy.Field()
