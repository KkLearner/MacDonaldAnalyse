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
    macDonaldId = scrapy.Field() #所属麦当劳id
    trafficName = scrapy.Field() #交通设施名称
    trafficlat = scrapy.Field() #纬度
    trafficlng = scrapy.Field() #经度
    trafficLine = scrapy.Field() #交通路线情况
    trafficuid = scrapy.Field() #设施uid
    distance = scrapy.Field() #距离中心点距离

class MacDonaldItem(scrapy.Item):
    name = scrapy.Field() #名称
    lat = scrapy.Field() #纬度
    lng = scrapy.Field() #经度
    address = scrapy.Field() #具体地址
    uid = scrapy.Field() #uid
    detail_url = scrapy.Field() #详情url
    price = scrapy.Field() #平均价格
    overall_rating = scrapy.Field() #平均评价

class ParkingLotItem(scrapy.Item):
    macDonaldId = scrapy.Field()  # 所属麦当劳id
    parkingLotname = scrapy.Field() #停车场名字
    parkingLotlat = scrapy.Field() #纬度
    parkingLotlng = scrapy.Field() #经度
    parkingLotAdress = scrapy.Field() #具体地址
    parkingLotUid = scrapy.Field() #uid
    parkingLotDistance = scrapy.Field() #距离中心点距离


class Business_District_Item(scrapy.Item):
    # 爬取该麦当劳分店所在商圈的商户的数据
    business_district_name = scrapy.Field() #商圈名字
    shop_name = scrapy.Field()              # 店铺名称
    shop_mean_price = scrapy.Field()        # 店铺人均消费
    shop_review_num = scrapy.Field()        # 评论人数
    shop_rank_stars = scrapy.Field()        # 评价等级
    shop_tag= scrapy.Field()                # 标签
    shop_addr = scrapy.Field()              # 具体地址

class BaiduFoodItem(scrapy.Item):
    macDonaldId = scrapy.Field()  # 所属麦当劳id
    businessName = scrapy.Field() #商铺名
    businesslat = scrapy.Field() #商铺纬度
    businesslng = scrapy.Field() #商铺经度
    businessAddress = scrapy.Field() #商铺地址
    businessUid = scrapy.Field() #商铺uid
    businessDistance = scrapy.Field() #商铺离中心点距离
    businessDetail = scrapy.Field() #商铺详情
    businessPrice = scrapy.Field() #美食平均价格
    businessOverall_rating = scrapy.Field() #美食平均评价

class SchoolItem(scrapy.Item):
    macDonaldId = scrapy.Field()  # 所属麦当劳id
    schoolName = scrapy.Field() #学校名
    schoollat = scrapy.Field() #学校纬度
    schoollng = scrapy.Field() #学校经度
    schoolAddress = scrapy.Field() #学校地址
    schoolUid = scrapy.Field() #学校uid
    schoolDistance = scrapy.Field() #学校离中心点距离
    schoolDetail = scrapy.Field() #学校详情
    type = scrapy.Field() #学校类型
    total = scrapy.Field() #学校人数

class CommunityItem(scrapy.Item):
    macDonaldId = scrapy.Field()  # 所属麦当劳id
    communityName = scrapy.Field() #小区名
    communitylat = scrapy.Field() #小区纬度
    communitylng = scrapy.Field() #小区经度
    communityAddress = scrapy.Field() #小区地址
    communityUid = scrapy.Field() #小区uid
    communityDistance = scrapy.Field() #小区离中心点距离
    communityBaiduDetail = scrapy.Field() #小区在百度的详情
    communityOtherDetail = scrapy.Field()  # 小区在其他的详情
    communityPrice = scrapy.Field() #小区平均价格
    communityTotal = scrapy.Field() #小区总户数
    belong_mac = scrapy.Field()
    type = scrapy.Field()