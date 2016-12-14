#This system receives JSON payload from System 2 via SFTP and sends it to System 4 using Pyro4 and encrypts it using Compression with CRC
import hashlib
import pysftp
import Pyro4
import json
import sys
import zlib

#Code that receives the file via SFTP and places it in the local directory
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu','username':'ftpuser','password':'test1234','port':109}
try:
	with pysftp.Connection(**cinfo) as sftp:
		try:
			with sftp.cd('/home/ftpuser'):
				sftp.get('payload.json')
		except:
			print "File Transfer issue"
except Exception, err:
	print err
	
print "Received Data"

def checkHash(checksum):
	check = hashlib.md5(open('payload.json','rb').read()).hexdigest()
	if(check == checksum):	
		print("Passed checksum test")
	else:
		print("Failed checksum test")

#Saving payload
with open('payload.json') as json_data:
	data = json.load(json_data)

@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self):
		payload = json.dumps(data)
		fileRead = open('payload.json','rb').read()
		fileComp = zlib.compress(fileRead,9)
		f = open('compressed_payload_file','wb')
		f.write(fileComp)
		f.close()
		intCRCfileRead = zlib.crc32(fileRead)
		intCRCfileComp = zlib.crc32(fileComp)
		print("Payload checksum: " + str(intCRCfileRead))
		print("Payload compressed checksum: " + str(intCRCfileComp))
		return payload

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(GreetingMaker())
ns.register("example.greeting", uri)
daemon.requestLoop()


