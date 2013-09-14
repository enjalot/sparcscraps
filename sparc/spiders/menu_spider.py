from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sparc.items import SparcItem
import re

class MenuSpider(BaseSpider):
    name = "menu"
    allowed_domains = ["sparcsf.org"]
    start_urls = [
        "http://sparcsf.org/medicine/flowers"
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
        hxs = HtmlXPathSelector(response)

        rows = hxs.select('//div[@class="leftTable"]/ul')
        names = rows.select('li[@class="name"]/p[@class="top"]/text()').extract()
        inout = rows.select('li[@class="name"]/p[@class="bottom"]/text()').extract()

        def getPrices(column):
            prices = []
            for i,row in enumerate(column):
                num = row.select('p[@class="num"]/text()').extract()
                if(len(num)):
                    num = int(num[0])
                else:
                    num = -1
                prices += [num]
            return prices
        def getTHC(div):
            thc = div.select('text()').extract()[0]
            #print "thc", thc
            num = re.search('[1-9]+', thc)
            if num:
                thc = int(num.group(0))
            else:
                thc = -1
            return thc

        items = []
        for i,row in enumerate(rows):
            item = SparcItem()
            item['name'] = names[i]
            prices = getPrices(row.select('li[@class="price"]/div'))
            #print "PRICES", i, names[i], prices
            item['prices'] = prices
            thc = getTHC(row.select('li[@class="active"]/div[@id="THC"]'))
            #print "THC", i, thc
            item['thc'] = thc
            cbd = getTHC(row.select('li[@class="active"]/div[@id="CBD"]'))
            #print "CBD", i, cbd
            strain = row.select('li[@class="strain"]/p/text()').extract()[0]
            item['strain'] = strain
            #print "strain", strain
            items.append(item)
        return items
