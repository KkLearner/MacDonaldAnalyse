import scrapy,json,urllib,MySQLdb
from MacDonaldAnalyse.items import BaiduTrafficItem

class BaiduTrafficSpider(scrapy.Spider):
    name = 'Traffic'
    allowed_domains = ['map.baidu.com']
    ak = 'LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx'
    radius = 1000
    urlTraffic = 'http://api.map.baidu.com/place/v2/search?query=地铁站$公交站&location={0},{1}' \
                 '&radius={2}&output=json&ak={3}&scope=2&page_num={4}&page_size=20' \
                 '&radius_limit=true'
    start_urls = [urlTraffic]

    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            db='macdonald',
            user='root',
            passwd='',
            charset='utf8',
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()
        sql = 'select id,lat,lng from macdonalditem'
        self.cursor.execute(sql)
        self.macdonalds = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()

    def parse(self, response):
        for temp in self.macdonalds:
            request = scrapy.Request(self.urlTraffic.format(temp[1], temp[2]
                        , self.radius, self.ak, 0), callback=self.parseTraffic)
            request.meta['macdonald'] = temp
            request.meta['index'] = 0
            yield request

    def parseTraffic(self, response):
        print('交通', urllib.parse.unquote(response.url))
        print()
        result = json.loads(response.body)
        resultList = result.get('results', '')
        macdonald = response.meta['macdonald']
        if '' != resultList and len(resultList) > 0:
            for result in resultList:
                item = BaiduTrafficItem()
                item['macDonaldId'] = macdonald[0]
                item['trafficName'] = result['name']
                item['trafficlat'] = result['location']['lat']
                item['trafficlng'] = result['location']['lng']
                item['trafficLine'] = result['address']
                item['trafficuid'] = result['uid']
                item['distance'] = result['detail_info']['distance']
                yield item
            index = response.meta['index'] + 1
            request = scrapy.Request(self.urlTraffic.format(macdonald[1], macdonald[2]
                            , self.radius, self.ak, index), callback=self.parseTraffic)
            request.meta['macdonald'] = macdonald
            request.meta['index'] = index
            yield request
