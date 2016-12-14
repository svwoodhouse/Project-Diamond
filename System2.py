#This system receives the JSON payload from System 1 via Socket and sends it to System 3 via SFTP using a hash payload value check
import pysftp
import datetime
import ssl
import socket
import json
import hashlib
#from System3 import checkHash
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


#Receiving the JSON payload via socket
print("[x] Opening Socket")
log("[x] Opening Socket")

bindsocket = socket.socket()
bindsocket.bind(('',8226))
bindsocket.listen(5)

#Takes the ssl, verifies it
def receive_json_ssl(connstream, data):
	print "[x] Received JSON payload from System1!\n", data
	log("[x] Received JSON payload from System 1")
	f = open('payload.json','w')
	f.write(data)
	f.close()
	print("\n[x] Closing socket\n")
	log("Closing Socket")
	print("[x]  Hashing\n")
	log("[x] Hashing")

	#Creating a hash payload value
	checksum = hashlib.md5(open('payload.json','rb').read()).hexdigest()

	#Storing the hash payload value in a file for safe keeping
	f1 = open('checksum.txt','w')
	f1.write(checksum)
	f1.close()
	return False

def deal_with_client(connstream):
	data = connstream.read()
	while data:
		if not receive_json_ssl(connstream, data):
			break
		data = constream.read()

while True:
	newsocket, addr = bindsocket.accept()
	connstream = ssl.wrap_socket(newsocket,server_side=True,certfile="server.crt",keyfile="server.key")
	try:
		deal_with_client(connstream)
	finally:
		connstream.shutdown(socket.SHUT_RDWR)
		connstream.close() 

#Function for checking hash
#checkHash(checksum)
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
	

