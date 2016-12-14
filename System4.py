#System 4 recieves the JSON payload from System 3 via Pyro4 and sends the JSON payload to System 1 via RabbitMQ using AES Encryption
from Crypto.Cipher import AES
import pika
import json
import Pyro4
import zlib
import sys
#Recieves the JSON payload via Pyro4
with open('payload.json') as json_data:
	data = json.load(json_data)

d = json.dumps(data)

blah = Pyro4.Proxy("PYRONAME:example.greeting")
payload = blah.get_fortune()

fileRead = open('compressed_payload_file','rb').read()
fileDeComp = zlib.compress(fileRead)
f = open('decompressed_payload_file','wb')
f.write(fileDeComp)
f.close()
print("[x]Decompressed File!")
intCRCfileRead = zlib.crc32(fileRead)
intCRCfileDeComp = zlib.crc32(fileDeComp)
print("Payload checksum: " + str(intCRCfileRead))
print("Payload compressed checksum: " + str(intCRCfileDeComp))
		
#Sends the JSON payload via RabbitMQ using AES Encryption
#Encrypt the JSON payload using AES
print("[x] Encrypting JSON payload")
pad = b' '
print(pad)

obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
plaintext = payload.encode('utf-8')
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

