import scrapy,json,urllib,MySQLdb,re,logging
from scrapy.selector import Selector
from MacDonaldAnalyse.items import CommunityItem

class CommunitySpider(scrapy.Spider):
    name = 'Community'
    handle_httpstatus_list = [404]
    allowed_domains = ['map.baidu.com','fang.com','leju.com','anjuke.com','sina.com.cn',
                       'soufun.com']
    ak = 'LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx'
    radius = 1000
    url = 'http://api.map.baidu.com/place/v2/search?query=小区&location={0},{1}' \
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
        self.log = [{'logname':'community','filename':'loggerCommunity.log'},
               {'logname': 'done', 'filename': 'done.log'}]
        self.loggers = ['','']
        for i in range(len(self.log)):
            self.loggers[i] = logging.getLogger(self.log[i]['logname'])
            handler = logging.FileHandler(self.log[i]['filename'])
            handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s'))
            self.loggers[i].setLevel(logging.INFO)
            self.loggers[i].addHandler(handler)

    def parse(self, response):
        done = []
        with open(self.log[1]['filename'],'r') as f:
            for line in f:
                done.append(line.strip())
        for temp in self.macdonalds:
            if str(temp[0]) in done:
                continue
            request = scrapy.Request(self.url.format(temp[1], temp[2]
                        , self.radius, self.ak, 0), callback=self.parseCommunity)
            request.meta['macdonald'] = temp
            request.meta['index'] = 0
            yield request

    def parseCommunity(self, response):
        # print('小区', urllib.parse.unquote(response.url))
        # print()
        result = json.loads(response.body)
        resultList = result.get('results', '')
        macdonald = response.meta['macdonald']
        if '' != resultList and len(resultList) > 0:
            for result in resultList:
                item = CommunityItem()
                item['macDonaldId'] = macdonald[0]
                item['communityName'] = result['name']
                item['communitylat'] = result['location']['lat']
                item['communitylng'] = result['location']['lng']
                item['communityAddress'] = result['address']
                item['communityUid'] = result['uid']
                item['communityDistance'] = result['detail_info']['distance']
                item['communityBaiduDetail'] = result['detail_info'].get('detail_url', '')
                item['communityOtherDetail'] = ''
                item['communityPrice'] = result['detail_info'].get('price', None)
                item['communityTotal'] = None
                if item['communityBaiduDetail'] != '':
                    detail = scrapy.Request(item['communityBaiduDetail'], callback=self.parseDetail)
                    detail.meta['item'] = item
                    yield detail
            index = response.meta['index'] + 1
            if index <= 5:
                request = scrapy.Request(self.url.format(macdonald[1], macdonald[2]
                                , self.radius, self.ak, index), callback=self.parseCommunity)
                request.meta['macdonald'] = macdonald
                request.meta['index'] = index
                yield request
            else:
                self.loggers[0].info('%s is end', macdonald[0])
                self.loggers[1].info('%s', macdonald[0])
        else:
            self.loggers[0].info('%s is end',macdonald[0])
            self.loggers[1].info('%s', macdonald[0])

    def parseDetail(self,response):
        item = response.meta['item']
        sel = Selector(response)
        ahrefs = sel.xpath("//div[@class='partnernav']//a[@class='from']")
        if len(ahrefs) <= 0:
            yield item
        else:
            other = scrapy.Request(urllib.parse.unquote(ahrefs[0].re(r'url=([^&]*)')[0]), callback=self.parseOther)
            other.meta['item'] = item
            yield other

    def parseOther(self,response):
        item = response.meta['item']
        if response.status != 404:
            otherUrl = urllib.parse.unquote(response.url)
            item['communityOtherDetail'] = otherUrl
            sel = Selector(response)
            if 'fang.com' in otherUrl or 'soufun.com' in otherUrl:
                self.setItem(sel.xpath("//div[@class='Rbiginfo']") \
                             .xpath("//span[@class='prib']//text()").extract(), item, 'communityPrice')
                self.setItem(sel.xpath("//div[@class='Rinfolist']") \
                             .re(r'<strong>房屋总数</strong>([^</li>]*)'), item, 'communityTotal')
            elif 'anjuke.com' in otherUrl:
                html = response.body.decode('utf-8')
                index = html.find('comm_midprice')
                item['communityPrice'] = re.sub('\D', '', html[index + 16:index + 25])
                self.setItem(sel.xpath("//dd[@class='other-dd']")[1] \
                             .xpath(".//text()").extract(), item, 'communityTotal')
            elif 'gz.esf.leju.com' in otherUrl or 'sina.com.cn' in otherUrl:
                self.setItem(sel.xpath("//ul[@class='com-details-t0']//li"
                                       "[@class='t1']//span[@class='s2']//text()").extract(), item, 'communityPrice')
                item['communityTotal'] = sel.xpath("//div[@class='panelB']//td")[2] \
                    .xpath('.//text()').extract()[1]
        yield item

    def setItem(self, temp, item, name):
        if len(temp) > 0:
            item[name] = re.sub('\D', '', temp[0])