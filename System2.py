#This system receives the JSON payload from System 1 via Socket and sends it to System 3 via SFTP using a hash payload value check
import pysftp
import socket
import json
from System3 import checkHash

#Creating a hash payload value
checksum = hashlib.md5(open('payload.json','rb').read()).hexdigest()

#Storing the hash payload value in a file for safe keeping
f = open('checksum.txt','w')
f.write(checksum)
f.close()

#Receiving the JSON payload via socket
print("opening socket")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9000
s.bind((host,port))
s.listen(5)

connection, addr = s.accept()
conn_stream = ssl.wrap_socket(connection, server_side=True,certfile="server.crt", keyfile = "server.key")
payload = conn_stream.read(2048)

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
