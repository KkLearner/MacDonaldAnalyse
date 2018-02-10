import scrapy,re,json,uuid
from scrapy.selector import Selector
from MacDonaldAnalyse.items import CommunityItem
import urllib

class TestSpider(scrapy.Spider):
    name = 'Test'
    handle_httpstatus_list = [404]
    allowed_domains = ['map.baidu.com','fang.com','leju.com','anjuke.com','sina.com.cn',
                       'soufun.com','github.com']
    url = 'http://api.map.baidu.com/place/v2/search?query=麦当劳&output=json&ak=LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx&page_num=0&scope=2'
    baiduUrl = 'http://api.map.baidu.com/place/v2/search?query=%E5%B0%8F%E5%8C%BA&location=23.1527,113.262&radius=1000&output=json&ak=LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx&scope=2&radius_limit=true&page_size=20&page_num=0'
    communityUrl = 'http://api.map.baidu.com/place/v2/search?query=小区&location={0},{1}' \
                 '&radius={2}&output=json&ak={3}&scope=2&page_num={4}&page_size=20' \
                 '&radius_limit=true'
    index = 0
    info = {}
    ak = 'LI5syaP0yQLSsgDXdPkRXb0rMnEZBhOx'
    start_urls = [communityUrl]

    def parse(self, response):
        request = scrapy.Request(self.communityUrl.format(23.1279, 113.374
                , 1000, self.ak, 0), callback=self.parseCommunity)
        request.meta['index'] = 0
        yield request

    def parseCommunity(self, response):
        # print('小区', urllib.parse.unquote(response.url))
        # print()
        result = json.loads(response.body)
        resultList = result.get('results', '')
        if '' != resultList and len(resultList) > 0:
            for result in resultList:
                item = CommunityItem()
                item['macDonaldId'] = 14
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
                item['belong_mac'] = -1
                item['type'] = 0
                if item['communityBaiduDetail'] != '' and not self.info.get(item['communityUid'], None):
                    item['belong_mac'] = str(uuid.uuid1())[:23].replace('-', '')
                    self.info[item['communityUid']] = {'uuid': item['belong_mac'],
                                                       'communityOtherDetail': item['communityOtherDetail'],
                                                       'communityPrice': item['communityPrice'],
                                                       'communityTotal': item['communityTotal']}
                    detail = scrapy.Request(item['communityBaiduDetail'], callback=self.parseDetail)
                    detail.meta['item'] = item
                    yield detail
                elif item['communityBaiduDetail'] != '':
                    temp = self.info[item['communityUid']]
                    item['communityOtherDetail'] = temp['communityOtherDetail']
                    item['communityPrice'] = temp['communityPrice']
                    item['communityTotal'] = temp['communityTotal']
                    item['belong_mac'] = temp['uuid']
                    item['type'] = 1
                    yield item
            index = response.meta['index'] + 1
            if index <= 5:
                request = scrapy.Request(self.communityUrl.format(23.1279, 113.374
                    , 1000, self.ak,index),callback=self.parseCommunity)
                request.meta['index'] = index
                yield request

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
        print(urllib.parse.unquote(response.url), response.status)
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
            self.info[item['communityUid']] = {'uuid': item['belong_mac'],
                                               'communityOtherDetail': item['communityOtherDetail'],
                                               'communityPrice': item['communityPrice'],
                                               'communityTotal': item['communityTotal']}
        yield item

    def setItem(self, temp, item, name):
        if len(temp) > 0:
            item[name] = re.sub('\D', '', temp[0])
