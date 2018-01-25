import scrapy,json,re,urllib
from scrapy.selector import Selector
from MacDonaldAnalyse.items import BaiduItem,BaiduTrafficItem,ParkingLotItem

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['map.baidu.com']
    ak = 'LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx'
    index = 0
    distance = 1000
    url = 'http://api.map.baidu.com/place/v2/search?query=麦当劳&tag=美食&region=广州' \
              '&output=json&ak={0}&page_num={1}&scope=2&page_size=20'
    urlTraffic = 'http://api.map.baidu.com/place/v2/search?query={0}&location={1},{2}' \
                 '&radius={3}&output=json&ak={4}&scope=2&page_num={5}&page_size=20' \
                 '&radius_limit=true'
    start_urls = [url]

    def parse(self, response):
        result = scrapy.Request(self.url.format(self.ak,self.index),callback=self.parseBaidu)
        yield result

    def parseBaidu(self,response):
        print('麦当劳',urllib.parse.unquote(response.url))
        print()
        result = json.loads(response.body)
        resultList = result.get('results','')
        if '' != resultList and len(resultList) > 0:
            for result in resultList:
                item = BaiduItem()
                item['name'] = result['name']
                item['lat'] = result['location']['lat']
                item['lng'] = result['location']['lng']
                item['address'] = result['address']
                item['uid'] = result['uid']
                item['detail_url'] = result['detail_info'].get('detail_url','')
                item['price'] = result['detail_info'].get('price','')
                item['overall_rating'] = result['detail_info'].get('overall_rating','')
                item['traffic'] = []
                item['parking'] = []
                yield self.nextRequest(item,'地铁站$公交站',0)
            self.index = self.index + 1
            yield scrapy.Request(self.url.format(self.ak,self.index), callback=self.parseBaidu)

    def parseTraffic(self,response):
        print(response.meta['keyword'],urllib.parse.unquote(response.url))
        print()
        jsonTraffic = json.loads(response.body)
        baidu = response.meta['item']
        trafficResult = jsonTraffic.get('results','')
        keyword = response.meta['keyword']
        if '' != trafficResult and len(trafficResult) > 0:
            hasNext = True
            for result in trafficResult:
                if result['detail_info']['distance'] <= self.distance:
                    if keyword == '地铁站$公交站':
                        self.setBaiduTrafficItem(result,baidu)
                    else:
                        self.setParkingLotItem(result,baidu)
                else:
                    hasNext = False
                    break
            if hasNext:
                yield self.nextRequest(baidu, keyword, response.meta['nextIndex'] + 1)
            elif keyword == '地铁站$公交站':
                yield self.nextRequest(baidu,'停车场',0)
            else:
                yield baidu
        elif keyword == '地铁站$公交站':
            yield self.nextRequest(baidu,'停车场',0)
        else:
            yield baidu

    def nextRequest(self,baidu,keyword,nextIndex):
        request = scrapy.Request(self.urlTraffic.format(keyword, baidu['lat'], baidu['lng']
                                        , self.distance, self.ak, nextIndex), callback=self.parseTraffic)
        request.meta['keyword'] = keyword
        request.meta['nextIndex'] = nextIndex
        request.meta['item'] = baidu
        return request

    def setBaiduTrafficItem(self,result,baidu):
        item = BaiduTrafficItem()
        item['trafficName'] = result['name']
        item['trafficlat'] = result['location']['lat']
        item['trafficlng'] = result['location']['lng']
        item['trafficLine'] = result['address']
        item['trafficuid'] = result['uid']
        item['distance'] = result['detail_info']['distance']
        baidu['traffic'].append(dict(item))

    def setParkingLotItem(self,result,baidu):
        item = ParkingLotItem()
        item['parkingLotname'] = result['name']
        item['parkingLotlat'] = result['location']['lat']
        item['parkingLotlng'] = result['location']['lng']
        item['parkingLotAdress'] = result['address']
        item['parkingLotUid'] = result['uid']
        item['parkingLotDistance'] = result['detail_info']['distance']
        baidu['parking'].append(dict(item))