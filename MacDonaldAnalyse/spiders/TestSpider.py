import scrapy
from MacDonaldAnalyse.items import ScrapytestItem
import urllib

class TestSpider(scrapy.Spider):
    name = 'Test'
    allowed_domains = ['baidu.com']
    url = 'http://api.map.baidu.com/place/v2/search?query=麦当劳&output=json&ak=LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx&page_num=0&scope=2'
    baiduUrl = 'https://www.baidu.com/'
    index = 0
    ak = 'LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx'
    start_urls = [baiduUrl]

    def parse(self, response):
        for i in range(5):
            item = ScrapytestItem()
            item['name'] = i
            item['list'] = []
            item['set'] = []
            request = scrapy.http.Request(self.baiduUrl, callback=self.setList, dont_filter=True)
            request.meta['item'] = item
            request.meta['listindex'] = 0
            yield request


    def setList(self,response):
        item = response.meta['item']
        listindex = response.meta['listindex']
        item['list'].append(listindex)
        listindex = listindex + 1
        if listindex <= 3:
            request = scrapy.http.Request(self.baiduUrl, callback=self.setList,dont_filter=True)
            request.meta['item'] = item
            request.meta['listindex'] = listindex
            yield request
        else:
            request = scrapy.http.Request(self.baiduUrl, callback=self.setSet, dont_filter=True)
            request.meta['item'] = item
            request.meta['setindex'] = 0
            yield request

    def setSet(self,response):
        item = response.meta['item']
        setindex = response.meta['setindex']
        item['set'].append(setindex)
        setindex = setindex + 1
        if setindex <= 3:
            request = scrapy.http.Request(self.baiduUrl, callback=self.setSet, dont_filter=True)
            request.meta['item'] = item
            request.meta['setindex'] = setindex
            yield request
        else:
            yield item


