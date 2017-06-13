import pika
from scrapy.http import HtmlResponse
import redis

tag_dict = {}

conn = redis.Redis()

def callback(ch, method, properties, body):
    response = body.decode('utf-8')
    url = response.split('\n')[0]
    response = HtmlResponse(url=url, body=response[len(url):], encoding='utf-8')
    title = response.css('.header .title::text').extract_first()
    difficulty = title[0] if title is not None else None
    if title is not None:
        title = title[3:]
        tags = response.css('.tag-box::text').extract()
        contest_name = response.css('.left a::text').extract()[0]
        for i in tags:
            conn.sadd("tags", i.strip())
            conn.sadd("tags_tmp", i.strip())
            conn.sadd(i.strip(), url)

        conn.hset(url, "name", title)
        conn.hset(url, "tags", conn.smembers("tags_tmp"))
        conn.delete("tags_tmp")
        if 'Div. 1' in contest_name:
            difficulty = "1" + difficulty
            conn.sadd(difficulty, url)
        else:
            if 'Div. 2' in contest_name:
                if difficulty >= 'C':
                    difficulty = "1" + chr(ord(difficulty) - 2)
                    conn.sadd(difficulty, url)
                else:
                    difficulty = "2" + difficulty
                    conn.sadd(difficulty, url)
            else:
                difficulty = "1" + difficulty
                conn.sadd(difficulty, url)
        conn.hset(url, "difficulty", difficulty)
        conn.sadd("difficulties", difficulty)
        print ('done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='response_queue', durable=True)

channel.basic_consume(callback,
                      queue='response_queue')

channel.basic_qos(prefetch_count=1)
channel.start_consuming()

connection.close()