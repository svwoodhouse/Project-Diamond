#This system receives JSON payload from System 2 via SFTP and sends it to System 4 using Pyro4 and encrypts it using Compression with CRC

import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu','username':'ftpuser','password':'test1234','port':109}
try:
	with pysftp.Connection(**cinfo) as sftp:
		try:
			sftp.cd('/home/ftpuser')
			data = sftp.get('payload.json')
			sftp.close()
			print(data)
		except:
			print "File Transfer issue"
except Exception, err:
	print err
	

print "Received Data"