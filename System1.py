#This system recieves the JSON payload from System 1 via RabbitMQ and sends it to System 2 via Socket programmig
import json
import socket
import ssl
import pika
import socket
from Crypto.Cipher import AES

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='json')

def callback(ch, method, properties, body):
	print("[x] Received JSON")
	print("Decrypting message")
	obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
	
	json_payload = obj.decrypt(body)
	print(json_payload)

	print("Ending RabbitMQ")
	channel.close()
	connection.close()

#sending the JSON payload via socket
	print("Sending payload via socket")
	socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssl_socket = ssl.wrap_socket(socket_client, ca_certs = "server.crt",cert_reqs = ssl.CERT_REQUIRED)
	host = socket.gethostname()
	port = 9000
	ssl_socket.connect((host,port))
	ssl_socket.write(json_payload)
	ssl_socket.close()
	print("Sent JSON payload")

channel.basic_consume(callback, queue='json', no_ack=True)


print('[*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()


