#This system receives JSON payload from System 2 via SFTP and sends it to System 4 using Pyro4 and encrypts it using Compression with CRC
import hashlib
import pysftp
import Pyro4
import json
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


@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self):
		with open('payload.json') as json_data:
			data = json.load(json_data)
		d = json.dumps(data)
		return d


daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(GreetingMaker)   # register the greeting maker as a Pyro object
ns.register("example.greeting", uri)   # register the object with a name in the name server

print("[x] Sending JSON payload via Pyro4!")
daemon.requestLoop()  
