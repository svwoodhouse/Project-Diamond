#This system receives the JSON payload from System 1 via Socket and sends it to System 3 via SFTP using a hash payload value check
import pysftp
import ssl
import socket
import json
import hashlib
from System3 import checkHash

#Creating a hash payload value
checksum = hashlib.md5(open('payload.json','rb').read()).hexdigest()

#Storing the hash payload value in a file for safe keeping
f = open('checksum.txt','w')
f.write(checksum)
f.close()

#Receiving the JSON payload via socket
print("opening socket")

bindsocket = socket.socket()
bindsocket.bind(('',8224))
bindsocket.listen(5)

True

#Takes the ssl, verifies it
def receive_json_ssl(connstream, data):
	print "Received payload!", data
	f = open('payload.json','w')
	f.write(data)
	f.close()
	return False

def deal_with_client(connstream):
	data = connstream.read()
	while data:
		if not receive_json_ssl(connstream, data):
			break
		data = constream.read()

while True:
	newsocket, addr = bindsocket.accept()
	connstream = ssl.wrap_socket(newsocket, server_side = True, certfile="server.crt", keyfile="server.key")
	try:
		deal_with_client(connstream)
	finally:
		connstream.shutdown(socket.SHUT_RDWR)
		connstream.close() 
print("Closing socket")
print("SFTP turn")

#Code that sends the JSON payload via SFTP 
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu','username':'ftpuser','password':'test1234','port':109}
try:
	with pysftp.Connection(**cinfo) as sftp:
		try:
			with sftp.cd('/home/ftpuser'):
				sftp.put('payload.json')
		except:
			print "File Transfer issue"
except Exception, err:
	print err
	
#Function for checking hash
checkHash(checksum)
