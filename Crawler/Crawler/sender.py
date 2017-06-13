import pika
import sys

message = ' '.join(sys.argv[1:]) or "Hello World!"
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='taskqueue', durable=True)

channel.basic_publish(exchange='',
                      routing_key='taskqueue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)

connection.close()