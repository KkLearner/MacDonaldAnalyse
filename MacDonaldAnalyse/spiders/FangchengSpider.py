import scrapy
from scrapy.selector import Selector
from MacDonaldAnalyse.items import FangchengItem

class FangchengSpider(scrapy.Spider):
    name = 'Fangcheng'
    allowed_domains = ['fangcheng.cn']

    def start_requests(self):
        urls = []
        for i in range(1,6):
            if i != 2:
                for j in (3,5):
                    urls.append(scrapy.Request('http://www.fangcheng.cn/details/slot?population=%s'
                                '&distance=%s&id=2&mall_id=362'%(i,j)))
        return urls

    def parse(self, response):
        sel = Selector(response)
        item = FangchengItem()
        item['title'] = sel.xpath('//select[@class="population"]').re(r'<option.*?selected>(.*)</option>')
        item['radius'] = sel.xpath('//select[@class="distance"]').re(r'<option.*?selected>(.*)</option>')
        list = sel.xpath("//div[@class='detail_buss_around_info']").xpath('//p')
        number = ''
        for i in range(len(list)):
            em = list[i].xpath('.//em')
            for j in range(len(em)):
                parent = em[j].xpath('..//text()').extract()
                number = number + parent[0] + parent[1] + parent[2]
                if j != len(em)-1:
                    number = number + ','
                else:
                    number = number + '.'
        item['number'] = number
        return item


