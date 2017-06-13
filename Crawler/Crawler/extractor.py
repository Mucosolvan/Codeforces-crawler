import pika
import requests

def callback(ch, method, properties, body):
    url = body.decode("utf-8")
    response = requests.get(body.decode("utf-8"))
    channel.basic_publish(exchange='',
                          routing_key='response_queue',
                          body=url+'\n'+response.text,
                          properties=pika.BasicProperties(
                            delivery_mode=2,  # make message persistent
                           ))
    print ('Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='link_queue', durable=True)
channel.queue_declare(queue='response_queue', durable=True)

channel.basic_consume(callback,
                      queue='link_queue')

channel.basic_qos(prefetch_count=1)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

connection.close()