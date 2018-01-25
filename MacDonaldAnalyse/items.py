# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    list = scrapy.Field()
    set = scrapy.Field()

class FangchengItem(scrapy.Item):
    title = scrapy.Field()
    radius = scrapy.Field()
    number = scrapy.Field()

class BaiduTrafficItem(scrapy.Item):
    trafficName = scrapy.Field() #交通设施名称
    trafficlat = scrapy.Field() #纬度
    trafficlng = scrapy.Field() #经度
    trafficLine = scrapy.Field() #交通路线情况
    trafficuid = scrapy.Field() #设施uid
    distance = scrapy.Field() #距离中心点距离

class BaiduItem(scrapy.Item):
    name = scrapy.Field() #名称
    lat = scrapy.Field() #纬度
    lng = scrapy.Field() #经度
    address = scrapy.Field() #具体地址
    uid = scrapy.Field() #uid
    detail_url = scrapy.Field() #详情url
    price = scrapy.Field() #平均价格
    overall_rating = scrapy.Field() #平均评价
    traffic = scrapy.Field() #交通设施--BaiduTrafficItem
    parking = scrapy.Field() #停车场--ParkingLotItem

class ParkingLotItem(scrapy.Item):
    parkingLotname = scrapy.Field() #停车场名字
    parkingLotlat = scrapy.Field() #纬度
    parkingLotlng = scrapy.Field() #经度
    parkingLotAdress = scrapy.Field() #具体地址
    parkingLotUid = scrapy.Field() #uid
    parkingLotDistance = scrapy.Field() #距离中心点距离
