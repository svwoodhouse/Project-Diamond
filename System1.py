#this system recieves the JSON payload from System 4 via RabbitMQ and sends it to System 2 via Socket programming

import json
import socket
import ssl
import pika
import socket
import datetime
from Crypto.Cipher import AES
from pymongo import MongoClient
from pymongo import ASCENDING
		
#Sets up Mongo for logging
mongoLogs = MongoClient().dbSydneeWoodhouse
db = mongoLogs.diamond_logs
log_collection = db.log_collection
log_collection.ensure_index([("timestamp", ASCENDING)])

def log(msg):
	entry = {}
	entry['timestamp'] = datetime.datetime.utcnow()
	entry['msg'] = msg
	log_collection.insert(entry)

#Receives the JSON payload by RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='json')

def callback(ch, method, properties, body):
	print("[x] Received JSON payload from System 4")
	print("Decrypting message")
	log('[x] Received JSON payload from System 4')
	log('[x] Decrypting message')

	obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	
	json_payload = obj.decrypt(body)
	print(json_payload)

	print("Ending RabbitMQ")
	log("Ending RabbitMQ")

	#sending the JSON payload via socket
	print("Sending JSON payload by Socket")
	log("Sending payload by Socket")

	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssl_sock = ssl.wrap_socket(s,ca_certs="server.crt",cert_reqs=ssl.CERT_REQUIRED)

	ssl_sock.connect(('localhost',8226))
	ssl_sock.write(json_payload)
	ssl_sock.close()

	print("[x] System 1 sent JSON payload by Socket")
	log("[x] System 1 sent JSON payload by Socket")

channel.basic_consume(callback, queue='json', no_ack=True)


print('[*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
