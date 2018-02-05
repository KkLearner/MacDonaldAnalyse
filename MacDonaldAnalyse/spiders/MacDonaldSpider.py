import scrapy,json,urllib
from MacDonaldAnalyse.items import MacDonaldItem

class MacDonaldSpider(scrapy.Spider):
    name = 'MacDonald'
    allowed_domains = ['map.baidu.com']
    ak = 'LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx'
    index = 0
    distance = 1000
    url = 'http://api.map.baidu.com/place/v2/search?query=麦当劳&tag=美食&region=广州' \
          '&output=json&ak={0}&page_num={1}&scope=2&page_size=20&city_limit=true'
    start_urls = [url]

    def parse(self, response):
        result = scrapy.Request(self.url.format(self.ak, self.index), callback=self.parseMacDonald)
        yield result

    def parseMacDonald(self, response):
        print('麦当劳', urllib.parse.unquote(response.url))
        print()
        result = json.loads(response.body)
        resultList = result.get('results', '')
        if '' != resultList and len(resultList) > 0:
            for result in resultList:
                item = MacDonaldItem()
                item['name'] = result['name']
                item['lat'] = result['location']['lat']
                item['lng'] = result['location']['lng']
                item['address'] = result['address']
                item['uid'] = result['uid']
                item['detail_url'] = result['detail_info'].get('detail_url', '')
                item['price'] = result['detail_info'].get('price', None)
                item['overall_rating'] = result['detail_info'].get('overall_rating', None)
                yield item
            self.index = self.index + 1
            yield scrapy.Request(self.url.format(self.ak, self.index), callback=self.parseMacDonald)