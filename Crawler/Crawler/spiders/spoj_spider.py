from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

tag_dict = {}

class SpojSpider(scrapy.Spider):
    name = "Spoj"

    start_urls = [
         'http://www.spoj.com/problems/classical/'
    ]

    tag_dict = {}

    def parse(self, response):
        for pages in response.xpath('//td[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//a').extract():
            href = pages.split('"')[1]
            #print (pages, href)
            yield scrapy.Request(response.urljoin(href), callback=self.parse_problem)

        pages_count = response.xpath('//li[(((count(preceding-sibling::*) + 1) = 15) and parent::*)]//*'
                                     '[contains(concat( " ", @class, " " ), concat( " ", "pager_link", " " ))]')
        if pages_count.extract_first() is not None:
            pages_count = int(pages_count.extract_first().split('=')[3].split('"')[0]) // 50
            for page_number in range(1, pages_count + 1):
                href = 'sort=0,start=%s' % str(page_number * 50)
                yield scrapy.Request(response.urljoin(href), callback=self.parse)

    def parse_problem(self, response):
        url = response.url
        title = response.css('#problem-name::text').extract_first()
        tags = [i[1:] for i in response.css('.problem-tag::text').extract()]

        for tag in tags:
            if tag not in tag_dict:
                tag_dict[tag] = []
            tag_dict[tag].append((url, title))

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

runner = CrawlerRunner()
d = runner.crawl(SpojSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()

for k, v in tag_dict.items():
    print (k)
