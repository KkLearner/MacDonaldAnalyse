# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Business_District_Item(scrapy.Item):
    # 爬取该麦当劳分店所在商圈的商户的数据
    business_district_name = scrapy.Field() #商圈名字
    shop_name = scrapy.Field()              # 店铺名称
    shop_mean_price = scrapy.Field()        # 店铺人均消费
    shop_review_num = scrapy.Field()        # 评论人数
    shop_rank_stars = scrapy.Field()        # 评价等级
    shop_tag= scrapy.Field()                # 标签
    shop_addr = scrapy.Field()              # 具体地址

