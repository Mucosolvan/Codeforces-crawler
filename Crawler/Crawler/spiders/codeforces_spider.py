from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import pika
import json

tag_dict = {}
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

class CodeforcesSpider(scrapy.Spider):
    name = "Codeforces"

    start_urls = [
         'http://codeforces.com/problemset/page/1'
    ]

    tag_dict = {}
    channel = connection.channel()

    channel.queue_declare(queue='link_queue', durable=True)
    def parse(self, response):
        for pages in response.css('td').css('.id'):
            href = pages.re('"/[a-zA-Z0-9/+]+"')[0].strip('"')
            self.channel.basic_publish(exchange='',
                                       routing_key='link_queue',
                                       body=response.urljoin(href),
                                       properties=pika.BasicProperties(
                                           delivery_mode=2,  # make message persistent
                                       ))

        pages_count = int(response.css('.page-index a::text')[-1].extract())
        for page_number in range(1, pages_count + 1):
            href = str(page_number)
            yield scrapy.Request(response.urljoin(href), callback=self.parse)

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

runner = CrawlerRunner()
d = runner.crawl(CodeforcesSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()

for k, v in tag_dict.items():
    print (k)

connection.close()