import scrapy,json,urllib,MySQLdb
from MacDonaldAnalyse.items import SchoolItem

class SchoolSpider(scrapy.Spider):
    name = 'School'
    allowed_domains = ['map.baidu.com']
    ak = 'LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx'
    radius = 1000
    tag = {"教育培训;高等院校": 0, "教育培训;中学": 1,
           "教育培训;小学": 2, "教育培训;幼儿园": 3,
           "教育培训;成人教育": 4, "教育培训;亲子教育":5 ,
           "教育培训;特殊教育学校": 6, "教育培训;留学中介机构": 7,
           "教育培训;科研机构": 8, "教育培训;培训机构": 9,
           "教育培训;图书馆": 10, "教育培训;科技馆": 11
           }
    url = 'http://api.map.baidu.com/place/v2/search?query=学校&location={0},{1}' \
                 '&radius={2}&output=json&ak={3}&scope=2&page_num={4}&page_size=20' \
                 '&radius_limit=true'
    start_urls = [url]

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
            request = scrapy.Request(self.url.format(temp[1], temp[2]
                        , self.radius, self.ak, 0), callback=self.parseSchool)
            request.meta['macdonald'] = temp
            request.meta['index'] = 0
            yield request

    def parseSchool(self, response):
        print('学校', urllib.parse.unquote(response.url))
        print()
        result = json.loads(response.body)
        resultList = result.get('results', '')
        macdonald = response.meta['macdonald']
        if '' != resultList and len(resultList) > 0:
            for result in resultList:
                item = SchoolItem()
                item['macDonaldId'] = macdonald[0]
                item['schoolName'] = result['name']
                item['schoollat'] = result['location']['lat']
                item['schoollng'] = result['location']['lng']
                item['schoolAddress'] = result['address']
                item['schoolUid'] = result['uid']
                item['schoolDistance'] = result['detail_info']['distance']
                item['schoolDetail'] = result['detail_info'].get('detail_url', '')
                item['type'] = self.tag.get(result['detail_info']['tag'], None)
                item['total'] = None
                yield item
            index = response.meta['index'] + 1
            if index <= 4:
                request = scrapy.Request(self.url.format(macdonald[1], macdonald[2]
                                , self.radius, self.ak, index), callback=self.parseSchool)
                request.meta['macdonald'] = macdonald
                request.meta['index'] = index
                yield request
