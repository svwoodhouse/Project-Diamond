#Sends the JSON payload via RabbitMQ using AES Encryption
#Encrypt the JSON payload using AES
#Recieves the JSON payload via Pyro4
from Crypto.Cipher import AES
import pika
import json
import Pyro4
import zlib
with open('payload.json') as json_data:
	data = json.load(json_data)

d = json.dumps(data)

print("[x] Encrypting JSON payload")
pad = b' '
print(pad)

obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
#plaintext = d.encode('utf-8')
plaintext = d.encode('utf-8')
length = 16 - (len(plaintext)%16)
plaintext += length*pad
ciphertext = obj.encrypt(plaintext) 
print plaintext
print("[x] Complete encryption, sending message!")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='json')

channel.basic_publish(exchange='',routing_key='json',body= ciphertext)

print('[x] Sent JSON payload')

connection.close()

