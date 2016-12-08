#This system receives the JSON payload from System 1 via Socket and sends it to System 3 via SFTP using a hash payload value check
import pysftp
import socket
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

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

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu','username':'ftpuser','password':'test1234','port':109}
try:
	with pysftp.Connection(**cinfo) as sftp:
		try:
			sftp.cd('/home/ftpuser')
			sftp.put('payload.json','/home/SydneeWoodhouse/Diamond/payload.json')
		except:
			print "File Transfer issue"
except Exception, err:
	print err
	


