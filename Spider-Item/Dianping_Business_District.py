from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import Business_District_Item
import random  # 用于随机更换UserAgent
import json



class BusinessDistrictShop(Spider):
    name = "BusinessDistrictShop"
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36"
    ]

    headers = {
        'User-Agent': random.choice(user_agent_list)
    }

    def start_requests(self):
        File = open('DaZhongDianPing_json.txt')
        district_list = File.readlines() # 所有商圈信息的列表
        File.close()
        start_urls = []
        i = 0
        print(district_list)
        # 命令行调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for line in district_list:
            district_link = json.loads(line)
            cur_url = district_link['McDonalds_tag_href']
            yield Request(cur_url, headers=self.headers)

    def parse(self, response):
        # 命令行调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        item = Business_District_Item()
        shops = response.xpath('.//div[@id="McDonald-all-list"]/ul/li')
        for shop in shops:
            item['business_district_name'] = response.meta['business_district_name']  # 商圈名
            item['shop_name'] = shop.xpath('.//div[@class="tit"]/a/@title').extract_first()  # 店铺名称
            item['shop_mean_price'] = shop.xpath('.//div[@class="comment"]/a[@class="mean-price"]/b/text()').extract_first()  # 店铺人均消费
            item['shop_review_num'] = shop.xpath('.//div[@class="comment"]/a[@class="review-num"]/b/text()').extract_first()  # 评论人数
            item['shop_rank_stars'] = shop.xpath('.//div[@class="comment"]/span/@title').extract_first()  # 评价等级
            item['shop_tag'] = shop.xpath('.//div[@class="tag-addr"]/a[last()]/@href').extract_first()  # 标签背后的超链接
            item['shop_addr'] = shop.xpath('.//div[@class="tag-addr"]/span[@class="addr"]/text()').extract_first()  # 具体地址
            yield item








